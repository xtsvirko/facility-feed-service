from services.metadata_generate import MetadataGenerator


def test_mock_metadata_generator():
    metadata = MetadataGenerator.generate_metadata(["mock_feed.json.gz"])
    assert "generation_timestamp" in metadata
    assert "mock_feed.json.gz" in metadata["data_file"]
