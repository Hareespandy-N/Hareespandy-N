import unittest
from engine import SCENARIOS, run


class SyntheticEngineTests(unittest.TestCase):
    def test_normal_completes_after_all_handshakes(self):
        trace = run("normal")
        self.assertTrue(trace["complete"])
        self.assertIsNone(trace["alarm"])
        systems = {x["system"] for x in trace["events"]}
        self.assertEqual(systems, {"SCADA", "PLC", "ASRS", "AMR", "COBOT"})
        self.assertEqual(trace["events"][-1]["action"], "Complete job")

    def test_missing_rack_blocks_downstream(self):
        trace = run("missing_rack")
        self.assertFalse(trace["complete"])
        self.assertEqual(trace["alarm"], "CONTAINER_NOT_PRESENT")
        self.assertFalse(any(x["system"] == "COBOT" for x in trace["events"]))
        self.assertFalse(any(x["action"] == "Transport container" for x in trace["events"]))

    def test_plc_interlock_stops_dispatch(self):
        trace = run("plc_blocked")
        self.assertEqual(trace["alarm"], "PLC_INTERLOCK_BLOCKED")
        self.assertFalse(any(x["action"] == "Dispatch to pickup" for x in trace["events"]))

    def test_charger_feedback_blocks_charge_command(self):
        trace = run("charger_not_ready")
        self.assertEqual(trace["alarm"], "CHARGER_NOT_READY")
        self.assertFalse(any(x["action"] == "Enter charge staging" for x in trace["events"]))

    def test_time_order_and_scenarios(self):
        for scenario in SCENARIOS:
            trace = run(scenario)
            self.assertEqual(trace["demo"], "SYNTHETIC_ONLY")
            self.assertEqual([e["time_s"] for e in trace["events"]],
                             list(range(0, len(trace["events"]) * 2, 2)))
            self.assertEqual(trace["complete"], trace["alarm"] is None)


if __name__ == "__main__":
    unittest.main()
