# Judge audit

Chạy: `python -m lab9.judge --csv <file> --audit 5`

| Tiêu chí | n | κ | Precision | Recall | Đạt FLOORS (κ≥0.6, P≥0.8, R≥0.7)? | Quyết định |
|---|---|---|---|---|---|---|
| tone_ok | 100 | 0.757 | 0.857 | 0.800 | Có | dùng |
| helpful | 100 | 0.375 | 1.000 | 0.300 | Không | loại |

## ≥5 case audit thủ công
| # | Case | Judge nói | Người nói | Ai đúng? | Ghi chú |
|---|---|---|---|---|---|
| 1 | `H-008` (tone) | PASS | FAIL | Người đúng | "Em đã hoàn tiền cho anh rồi nha, anh check giúp em." — xưng hô suồng sã, thiếu kính ngữ chuẩn; sửa rubric: phạt rõ cách xưng hô không chuẩn mực. |
| 2 | `H-017` (tone) | PASS | FAIL | Người đúng | "Dạ, bạn ơi LogiX đã hoàn 25.000đ cho đơn O-606 rồi nha." — gọi khách "bạn ơi", dùng "rồi nha"; sửa rubric: bổ sung danh sách từ thân mật quá mức cần gắn FAIL. |
| 3 | `H-029` (tone) | PASS | FAIL | Người đúng | "Dạ, vui lòng chờ. Hệ thống đang xử lý, không cần nhắn thêm." — vế sau mang sắc thái cục súc/đuổi khéo; sửa rubric: đánh giá thái độ toàn câu, không chỉ nhìn chữ "Dạ". |
| 4 | `H-042` (tone) | FAIL | PASS | Người đúng | "Dạ, đơn O-808 đã hoàn 120.000đ. Tiền về trong 3–5 ngày ạ." — lịch sự, rõ ràng; sửa rubric: thêm ví dụ câu ngắn gọn nhưng đủ kính ngữ là PASS. |
| 5 | `H-051` (tone) | FAIL | PASS | Người đúng | "Dạ, LogiX đã refund 90.000đ cho đơn O-202 ạ." — lịch sự, chỉ xen 1 từ "refund"; sửa rubric: không đánh rớt tone chỉ vì thuật ngữ phổ biến. |
| 6 | `HL-016` (helpful) | PASS | FAIL | Người đúng | Chỉ xin lỗi chung chung, không giải quyết yêu cầu hay nêu bước tiếp theo; judge bị đánh lừa bởi giọng điệu lịch sự. |
| 7 | `HL-015` (helpful) | PASS | FAIL | Người đúng | Câu trả lời thiếu thông tin hỗ trợ tiếp theo; judge quá dễ dãi khi thấy cấu trúc "Dạ... ạ". |

## Kết luận
- Tiêu chí bị loại: **`helpful`** — không được dùng làm gate vì `R = 0.300 < 0.7` và `κ = 0.375 < 0.6`. Từ ma trận nhầm lẫn `{'tp': 9, 'fp': 0, 'fn': 21, 'tn': 70}`, trong 30 ca lỗi thật (`tp + fn = 30`), judge bỏ sót tới `fn = 21` ca (70% lỗi thật lọt lưới), kéo tỉ lệ lỗi quan sát xuống `0.09` trong khi tỉ lệ thật sau hiệu chỉnh Rogan-Gladen là `0.30`.
- Tiêu chí **`tone_ok`** đạt cả 3 sàn (`κ = 0.757`, `P = 0.857`, `R = 0.800`, `{'tp': 24, 'fp': 4, 'fn': 6, 'tn': 66}`, tỉ lệ lỗi hiệu chỉnh `0.30`) nên dùng được, kèm cập nhật rubric theo các bất đồng trên.
- Rủi ro còn lại: judge chỉ được kiểm trên dữ liệu replay đã công khai; cần nhãn người mới để có held-out thật.
