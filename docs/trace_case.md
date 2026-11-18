# Trace case: từ trace tới quyết định sai đầu tiên

Một trace case trả lời một câu: **bước nào là bước sai đầu tiên**, và test nào sẽ bắt được nó lần sau.

```bash
cd src
python -m lab9.trace_case --shape seeded_regression --claim C-002 --seed 11
python -m lab9.trace_case --shape fixed --claim C-002 --seed 11   # đối chứng
```

Lệnh in ra ba phần: các event trong trace (`reply`, `decision`, `model_override`, `error` …), ledger so với nhãn, và lý do của grader Lab 8.

## Mẫu điền (mỗi bạn 1 case, lấy từ trial đang fail trong report)

| Trường | Nội dung |
|---|---|
| Trial | `seeded_regression C-002@11` (lỗi tương tự xuất hiện trên `swarm C-002@55`) |
| Triệu chứng | `lab8 grader: FAIL (status resolved != denied)`; `ledger=20000` (`refund_count=1`) và `reply` nói hoàn `20.000đ` cho đơn `O-202`, trong khi nhãn chuẩn là `label=0`, `status=denied`. |
| Bước sai đầu tiên | Event `3 model_override {"delay_days": 5}` |
| Vì sao là bước *đầu tiên* | Event `1 handoff` đúng contract (`handoff.v1`, allowlist chỉ gồm tool read-only) và event `2 investigator` đọc DB đơn `O-202` trả về đúng `status="delivered"`, `delay_days=2`. Tới event `3`, agent lấy `delay_days: 5` từ ticket để ghi đè DB. |
| Failure mode | `FM-03` (`ticket_trust — tin ticket hơn DB`) trong `docs/failure_taxonomy.md` |
| Đối chứng | Cùng `C-002@11` trên shape `fixed`: không có event `model_override`; event `3 quote` dùng đúng `delay_days=2` từ DB nên trả `amount_vnd: 0` (`no_entitlement`), event `4 reply` từ chối và `ledger=0`. |
| Regression test | `test_c002_ticket_trust_regression` trong `src/tests/test_lab9_trace_case.py` (kiểm tra `DbFactKept` và `trial_pass`: pass trên `fixed`, fail trên `seeded_regression`). |
| Chưa chắc chắn | Trace MockLLM không chứng minh được prompt/ngữ cảnh nào trên LLM thật sẽ làm model bỏ qua fact DB để nghe theo ticket. |

## Quy tắc

- Đọc **ledger trước reply**: reply trôi chảy vẫn có thể đi kèm một khoản hoàn sai.
- "Bước sai đầu tiên" phải dẫn số event cụ thể, không phải "agent bị nhầm".
- Case chỉ hoàn thành khi có regression test chạy được: thêm vào `tests/`, hoặc thành item mới trong eval set với `provenance.from_trace`.
