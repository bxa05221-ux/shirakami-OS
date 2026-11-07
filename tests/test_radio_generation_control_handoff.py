"""Characterization tests for Radio generation-control handoff.

These tests document current behavior; they do not claim that the
end-to-end generation-control contract is implemented.
No provider calls, publication, or external side effects.
"""

import unittest

from runtime.adapter import PipelineAdapter
from runtime.oppai_runtime_flow import execute_selected_pipeline
from runtime.protocol_loader import ProtocolIR
from runtime.protocol_registry import ProtocolRegistry
from runtime.real_model_adapter import RealModelAdapter


class RadioGenerationControlHandoffTests(unittest.TestCase):
    def test_real_model_adapter_preserves_legacy_request_without_control(self):
        captured = []
        adapter = RealModelAdapter(lambda request: captured.append(request) or "fixture")
        output = adapter("今朝は風が冷たいです。", "shirakami-radio-v2.1")
        self.assertEqual(output, "fixture")
        self.assertEqual(len(captured), 1)
        request = captured[0]
        self.assertEqual(request.canonical_prompt, "今朝は風が冷たいです。")
        self.assertEqual(request.context, {"protocol_id": "shirakami-radio-v2.1"})
        self.assertNotIn("generation_control", request.context)
        self.assertNotIn("evaluation", request.context)
        self.assertNotIn("next_turn", request.context)

    def test_pipeline_control_reaches_provider_without_authority_or_mutation(self):
        registry = ProtocolRegistry()
        artifact = ProtocolIR(
            protocol_id="shirakami-radio-v2.1",
            title="Shirakami Radio",
            version="2.1",
            statement="Different views without forced semantic bridging.",
            pipeline=(
                {"phase": "listener", "action": "generate_independent_landscape"},
            ),
        )
        registry.register_temporary(artifact.protocol_id, artifact)
        captured = []
        adapter = RealModelAdapter(lambda request: captured.append(request) or "fixture")
        control = {
            "instructions": {"semantic_bridging": False},
            "human_authority": "preserved",
        }

        execution = execute_selected_pipeline(
            "今朝は風が冷たいです。",
            registry,
            artifact.protocol_id,
            PipelineAdapter(adapter.execute_pipeline, backend_id="model-fixture"),
            context={"generation_control": control, "broadcast_authorized": False},
        )

        self.assertEqual(execution.steps[0].output, "fixture")
        self.assertEqual(len(captured), 1)
        provider_request = captured[0]
        self.assertEqual(provider_request.canonical_prompt, "今朝は風が冷たいです。")
        self.assertEqual(provider_request.context["protocol_id"], artifact.protocol_id)
        self.assertEqual(
            provider_request.context["generation_control"],
            {
                "instructions": {"semantic_bridging": False},
                "human_authority": "preserved",
                "protocol_id": artifact.protocol_id,
                "protocol_version": "2.1",
                "phase": "listener",
                "action": "generate_independent_landscape",
            },
        )
        self.assertEqual(control, {
            "instructions": {"semantic_bridging": False},
            "human_authority": "preserved",
        })
        self.assertNotIn("execution_authorized", provider_request.context)
        self.assertNotIn("publish_authorized", provider_request.context)
        self.assertNotIn("merge_authorized", provider_request.context)

    def test_selected_pipeline_carries_step_metadata_to_mock_adapter(self):
        registry = ProtocolRegistry()
        artifact = ProtocolIR(
            protocol_id="shirakami-radio-v2.1",
            title="Shirakami Radio",
            version="2.1",
            statement="Different views without forced semantic bridging.",
            pipeline=(
                {"phase": "listener", "action": "generate_independent_landscape"},
                {"phase": "host", "action": "acknowledge_without_analysis"},
            ),
        )
        registry.register_temporary(artifact.protocol_id, artifact)
        captured = []
        adapter = PipelineAdapter(lambda request: captured.append(request) or {"ok": True}, backend_id="mock")
        execution = execute_selected_pipeline(
            "今朝は風が冷たいです。",
            registry,
            artifact.protocol_id,
            adapter,
            context={"broadcast_authorized": False},
        )
        self.assertEqual(len(execution.steps), 2)
        self.assertEqual(
            [request.action for request in captured],
            ["generate_independent_landscape", "acknowledge_without_analysis"],
        )
        self.assertTrue(all(request.context["broadcast_authorized"] is False for request in captured))
        self.assertTrue(all(request.protocol_id == artifact.protocol_id for request in captured))
        # Structural metadata delivery is not proof of behavioral compliance.
        self.assertNotIn("generation_control", captured[0].context)


if __name__ == "__main__":
    unittest.main()
