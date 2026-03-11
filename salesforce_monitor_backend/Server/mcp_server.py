from mcp.server.fastmcp import FastMCP
import requests

mcp = FastMCP("Salesforce Monitoring Tools")

API_BASE = "http://localhost:8012"

@mcp.tool()
def get_jobs():
    """Fetch current Salesforce jobs"""
    r = requests.get(f"{API_BASE}/jobs")
    return r.json()

@mcp.tool()
def get_failed_jobs():
    """Fetch failed Salesforce jobs"""
    r = requests.get(f"{API_BASE}/failed-jobs")
    return r.json()

@mcp.tool()
def get_system_health():
    """Run AI system health analysis"""
    r = requests.get(f"{API_BASE}/job-monitoring")
    return r.json()

@mcp.tool()
def run_limit_guard():
    """Run Salesforce limit guard monitoring"""
    r = requests.get(f"{API_BASE}/limit-guard")
    return r.json()

if __name__ == "__main__":
    mcp.run()


# {
#   "mcpServers": {
#     "salesforce-monitor": {
#       "command": "C:/All_Projects/PWC_OKT/PWC_CSX/PWC_CSX_First/salesforce-job-extractor/venv/Scripts/python.exe",
#       "args": [
#         "C:/All_Projects/PWC_OKT/PWC_CSX/PWC_CSX_First/salesforce-job-extractor/salesforce_monitor_backend/Server/mcp_server.py"
#       ]
#     }
#   }
# }