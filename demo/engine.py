"""Synthetic industrial workflow state-machine demo. No hardware/network I/O."""
from __future__ import annotations

import argparse
import json

SCENARIOS = ("normal", "missing_rack", "plc_blocked", "charger_not_ready")


def run(scenario: str = "normal") -> dict:
    """Return deterministic trace for a single simulated material movement."""
    if scenario not in SCENARIOS:
        raise ValueError(f"Unknown scenario: {scenario}")

    events = []
    def emit(system: str, action: str, status: str, detail: str) -> None:
        events.append({"time_s": len(events) * 2, "system": system,
                       "action": action, "status": status, "detail": detail})

    emit("SCADA", "Create job", "ok", "Synthetic transfer request received")
    emit("PLC", "Check machine interlocks", "ok" if scenario != "plc_blocked" else "fault",
         "Machine and transfer zone ready" if scenario != "plc_blocked" else "Transfer-zone interlock is not satisfied")
    if scenario == "plc_blocked":
        emit("AMR", "Hold mission", "hold", "No dispatch while PLC interlock is blocked")
        emit("SCADA", "Raise alarm", "fault", "PLC_INTERLOCK_BLOCKED")
        return _result(scenario, events, "PLC_INTERLOCK_BLOCKED")

    emit("ASRS", "Verify pickup container", "ok" if scenario != "missing_rack" else "fault",
         "Container located in requested storage slot" if scenario != "missing_rack" else "Requested container not detected")
    if scenario == "missing_rack":
        emit("AMR", "Hold mission", "hold", "Pickup cannot proceed without container")
        emit("SCADA", "Raise alarm", "fault", "CONTAINER_NOT_PRESENT")
        return _result(scenario, events, "CONTAINER_NOT_PRESENT")

    emit("AMR", "Dispatch to pickup", "ok", "Mission started (simulated)")
    emit("AMR", "Arrive at transfer point", "ok", "Position reached (simulated)")
    emit("ASRS", "Offer container", "ok", "Storage handoff ready")
    emit("PLC", "Confirm transfer I/O", "ok", "Request / ready / complete handshake observed")
    emit("AMR", "Transport container", "ok", "Delivery request accepted")
    emit("COBOT", "Receive material", "ok", "Robot cell ready and transfer acknowledged")
    emit("PLC", "Request charging clearance", "ok" if scenario != "charger_not_ready" else "fault",
         "Charger feedback permits approach" if scenario != "charger_not_ready" else "Charger readiness feedback missing")
    if scenario == "charger_not_ready":
        emit("AMR", "Hold charging step", "hold", "No charge command sent; await valid feedback")
        emit("SCADA", "Raise alarm", "fault", "CHARGER_NOT_READY")
        return _result(scenario, events, "CHARGER_NOT_READY")

    emit("AMR", "Enter charge staging", "ok", "Simulated charging sequence accepted")
    emit("SCADA", "Complete job", "ok", "End-to-end simulated workflow completed")
    return _result(scenario, events, None)


def _result(scenario: str, events: list[dict], alarm: str | None) -> dict:
    return {"demo": "SYNTHETIC_ONLY", "scenario": scenario,
            "complete": alarm is None, "alarm": alarm, "events": events}


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--scenario", choices=SCENARIOS, default="normal")
    cli.add_argument("--json", action="store_true", help="Print machine-readable trace")
    args = cli.parse_args()
    result = run(args.scenario)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        for item in result["events"]:
            print(f"{item['time_s']:>3}s  {item['system']:<6}  {item['status']:<5}  {item['action']}  — {item['detail']}")
        print("RESULT:", "COMPLETED" if result["complete"] else f"HELD ({result['alarm']})")
