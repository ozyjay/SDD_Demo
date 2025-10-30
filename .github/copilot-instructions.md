# Copilot Instructions for This Repository

## Project Context
- This is a specification-driven development workflow: we write our functional and acceptance requirements in `specifications/requirements.md` before implementation.
- We follow the tech stack: **Python 3 + PyGame + pygbag (WebAssembly)**
- All code is maintained in this repository and will be run in GitHub Codespaces via web browser.
- Code must be **async/await compatible** for pygbag browser deployment.

## Coding Standards & Preferences
- Naming conventions:  
  - Classes/Modules: `PascalCase`.  
  - Functions/Methods: `camelCase`.  
  - Constants: `UPPER_CASE`.  
- Formatting:  
  - Use **tabs** for indentation (or spaces—choose one).  
  - Max line length: 100 characters.  
  - Include meaningful doc comments for public APIs.  
- Testing:  
  - For each functional requirement in `specifications/requirements.md`, generate a corresponding unit/integration test.  
  - Test method names should follow `featureName_condition_expectedOutcome`.  
  - Use the test framework: PyTest
- Specification linking:  
  - When generating code, reference the requirement identifier from `requirements.md` (e.g., `REQ-001: User can log in`).  
  - Ensure mapping of requirement → code module → test is clear and traceable.

## Specification Source
All functional and non-functional requirements are defined in the `specifications/` folder.
When generating or modifying code, read the relevant sections from:
- `specifications/requirements.md`
- `specifications/acceptance_criteria.md`

Ensure generated code includes comments that reference the corresponding requirement ID (e.g., REQ-002).


## Implementation Guidance
- Generate code that strictly satisfies the functional and acceptance requirements in `specifications/requirements.md`.  
- **Ensure async/await compatibility** for pygbag: main game loop must use `async def` and `await asyncio.sleep(0)`.
- Include clear error handling, input validation, and logging according to our stack's best practices.  
- Adhere to the architectural layers: (e.g., Controller → Service → Repository) unless specified otherwise.  
- Provide inline comments only for non-obvious logic. Prefer readable code over comments.

## Review & Maintenance
- Always include a short description of how the change addresses requirement(s) (e.g., “Addresses REQ-005 and REQ-006”).  
- Ensure new code is covered by tests and that tests are passing locally in Codespaces.  
- Keep the spec file (`specifications/requirements.md`) up-to-date and link any changes to implementation/test updates.

