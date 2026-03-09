import salesforce_monitor_backend.Service.ai_metrics_engine as metrics_engine
import salesforce_monitor_backend.Service.anomaly_engine as anomaly_engine
import salesforce_monitor_backend.Service.root_cause_engine as root_engine
import salesforce_monitor_backend.Service.mitigation_engine as mitigation_engine
import salesforce_monitor_backend.Agent.ai_agent_main as ai_agent


class LimitGuardAgent:

    def run(self):

        # Step 1: observe system
        metrics, alerts, failed_jobs = metrics_engine.evaluate_main_system_health()

        # Step 2: detect anomalies
        anomalies = anomaly_engine.detect_anomalies(metrics)

        # Step 3: root cause analysis
        root_causes = root_engine.identify_top_failed_classes()

        # Step 4: AI reasoning
        ai_report = ai_agent.run_ai_analysis_structured_pydentic(
            metrics,
            alerts + anomalies,
            failed_jobs
        )

        # Step 5: mitigation recommendations
        actions = mitigation_engine.recommend_action(anomalies)

        return {
            "metrics": metrics,
            "anomalies": anomalies,
            "root_causes": root_causes,
            "ai_report": ai_report,
            "recommended_actions": actions
        }