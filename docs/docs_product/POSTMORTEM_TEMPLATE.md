# Postmortem Template — Vietstock Agent

> Dùng template này khi hệ thống gặp sự cố production.
> Copy file này và đổi tên theo format: `POSTMORTEM_YYYY-MM-DD_<short-description>.md`

---

## Incident Summary

- **Thời gian xảy ra:** YYYY-MM-DD HH:MM (UTC+7)
- **Thời gian phát hiện:** YYYY-MM-DD HH:MM
- **Thời gian khắc phục:** YYYY-MM-DD HH:MM
- **Tổng downtime:** X phút/giờ
- **Ảnh hưởng:**
  - Số user bị ảnh hưởng: —
  - Feature bị ảnh hưởng: —
  - Data loss: Có / Không
  - Severity: P0 / P1 / P2 / P3

---

## Root Cause

- **Vì sao lỗi:**
  (Mô tả chi tiết nguyên nhân gốc. Ví dụ: vnstock3 API thay đổi response format mà không báo trước, gây crash trong data parsing layer.)

- **Component liên quan:**
  (VD: Data Layer → vnstock3 adapter)

---

## Timeline

| Thời gian  | Sự kiện                                                  |
| ---------- | -------------------------------------------------------- |
| HH:MM      | Bắt đầu xảy ra lỗi                                      |
| HH:MM      | Alert triggered (monitoring detect)                       |
| HH:MM      | Team bắt đầu investigate                                 |
| HH:MM      | Xác định root cause                                      |
| HH:MM      | Deploy fix / rollback                                    |
| HH:MM      | Service recovered                                        |
| HH:MM      | Confirm stable                                           |

---

## Fix

- **Đã làm gì để khắc phục:**
  1. (VD: Rollback vnstock3 adapter về version trước)
  2. (VD: Patch data parser để handle format mới)
  3. (VD: Deploy hotfix version X.Y.Z)

- **PR/Commit:** (link to PR hoặc commit hash)

---

## Prevention

- **Thêm monitoring:**
  (VD: Alert khi vnstock3 response format thay đổi)

- **Improve test:**
  (VD: Integration test với mock vnstock3 responses, bao gồm format mới)

- **Process change:**
  (VD: Pin vnstock3 version trong requirements, review changelog trước khi upgrade)

- **Action items:**

| Action                                    | Owner       | Deadline   | Status |
| ----------------------------------------- | ----------- | ---------- | ------ |
| Thêm integration test cho data parsers    | —           | —          | TODO   |
| Thêm alert cho data source format change  | —           | —          | TODO   |
| Pin dependency versions                   | —           | —          | TODO   |

---

## Lessons Learned

- (VD: Không nên auto-update data source libraries mà không test)
- (VD: Cần có contract testing cho external APIs)
