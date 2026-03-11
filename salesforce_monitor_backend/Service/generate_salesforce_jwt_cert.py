from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography import x509
from cryptography.x509.oid import NameOID
import datetime

# Generate RSA private key
key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

# Save private key
with open("server.key", "wb") as f:
    f.write(
        key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
    )

# Certificate subject/issuer
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "State"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, "City"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Salesforce Integration"),
    x509.NameAttribute(NameOID.COMMON_NAME, "salesforce-jwt"),
])

# Build certificate
cert = (
    x509.CertificateBuilder()
    .subject_name(subject)
    .issuer_name(issuer)
    .public_key(key.public_key())
    .serial_number(x509.random_serial_number())
    .not_valid_before(datetime.datetime.now(datetime.timezone.utc))
    .not_valid_after(datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365))
    .sign(key, hashes.SHA256())
)

# Save certificate
with open("server.crt", "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))

print("✅ JWT certificate generated successfully!")
print("Files created:")
print(" - server.key (private key)")
print(" - server.crt (certificate)")