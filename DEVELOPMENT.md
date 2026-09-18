# Development Notes

This project was developed with an AI coding agent in VS Code.

The implementation was validated incrementally: the backend modules were compiled, API tests were run after the first backend slice, and a retrieval dependency compatibility issue was replaced with a pure-Python TF-IDF/cosine implementation. The focused tests cover authentication, authorization ownership, persistence, and structured decisions.

The supplied workspace contained only AppleDouble metadata under `__MACOSX`; the original candidate policy payload and sample CSV were not recoverable. A small representative policy corpus and evaluation set were therefore added under `knowledge_base/` and `sample_test_cases.json`. These files are intentionally simple and can be replaced by the supplied files without changing the API contract.
