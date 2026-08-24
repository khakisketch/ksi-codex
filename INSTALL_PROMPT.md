# New PC installation prompt

Copy the prompt below into Codex on the computer where this configuration should
be installed.

```text
내 개인 PC에 KSI Codex 휴대용 구성을 설치해 주세요.

배포 저장소:
https://github.com/khakisketch/ksi-codex

목표:
- 현재 PC의 Codex 전역 지침, read-only explorer 에이전트, command rules,
  휴대 가능한 기본 설정을 안전하게 설치합니다.
- 이 작업은 로컬 Codex 설정 설치만 허용합니다. 프로젝트 코드 변경이나
  원격 저장소 쓰기, 임의의 플러그인/OAuth 연결은 하지 마세요.

진행 규칙:
1. 먼저 OS, Codex CLI, Git, GitHub CLI, Python 3.11+, Node.js/npx 설치 여부를
   읽기 전용으로 확인하세요.
2. GitHub CLI가 로그인되어 있지 않으면 제가 직접 `gh auth login`을 완료할
   때까지 기다리세요. 토큰, 비밀번호, OTP를 요청하거나 출력하지 마세요.
3. 비공개 저장소 `khakisketch/ksi-codex`를 사용자 홈 아래 `ksi-codex`로
   clone하거나, 이미 있으면 origin과 변경 상태를 확인한 뒤 `git pull --ff-only`만
   사용하세요. 로컬 변경이 있으면 덮어쓰지 말고 보고하세요.
4. 저장소의 `AGENTS.md`, `README.md`, `CURRENT_STATE.md`, `docs/install.md`를 읽고 적용 범위를
   확인하세요.
5. 다음 명령으로 반드시 dry-run을 먼저 수행하세요:
   `./install.sh --dry-run --mode copy --config-mode replace --backup`
6. dry-run 대상이 아래 범위를 벗어나면 중단하세요:
   - ~/.codex/AGENTS.md
   - ~/.codex/agents/explorer.toml
   - ~/.codex/rules/ksi-default.rules
   - ~/.codex/config.toml
   - ~/.codex/backups/
7. 이 PC는 개인 개발 PC이며, 저장소에 문서화된
   `approval_policy = "never"`와 `sandbox_mode = "danger-full-access"` 적용을
   승인합니다. 기존 파일은 반드시 백업한 뒤 다음 명령으로 설치하세요:
   `./install.sh --mode copy --config-mode replace --backup`
8. 다음 검증을 실행하세요:
   - `python3 -m py_compile scripts/apply.py scripts/check.py scripts/uninstall.py`
   - `python3 scripts/check.py --source-only --skip-mcp`
   - `python3 scripts/check.py`
   - `codex --version`
   - `codex mcp list`
9. auth.json, 세션, history, SQLite, memories, 브라우저 프로필, 캐시,
   쿠키, API 키, 토큰, 비밀번호, OTP, private key는 복사하거나 Git에 넣지 마세요.
10. 플러그인과 OAuth 연결은 설정 파일만으로 복제됐다고 주장하지 마세요.
    필요한 로그인은 제가 Codex UI에서 직접 수행하도록 목록만 알려주세요.
11. 설치 후 Codex 재시작이 필요하다고 알려주고, 설치된 파일, 생성된 백업,
    검증 결과, 남은 수동 로그인/연결 작업을 한국어로 요약하세요.

오류가 발생하면 기존 설정을 삭제하거나 강제로 덮어쓰지 말고, 정확한 오류와
안전한 복구 방법을 보고하세요.
```
