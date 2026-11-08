"""
VFX Shot Tracker - เวอร์ชัน 1 (เทอร์มินัล)
สัปดาห์ที่ 1: เรียนรู้ตัวแปร ลิสต์ dict ลูป ฟังก์ชัน และการอ่าน/เขียนไฟล์

วิธีรัน:  python shot_tracker.py
"""

import json
import os

DATA_FILE = "shots.json"  # ไฟล์ที่ใช้เก็บข้อมูล
STATUSES = ["Todo", "In Progress", "Review", "Done"]


# ---------- ส่วนที่ 1: อ่าน/เขียนไฟล์ ----------

def load_shots():
    """อ่านรายการ shot จากไฟล์ ถ้ายังไม่มีไฟล์ให้คืนลิสต์ว่าง"""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_shots(shots):
    """บันทึกรายการ shot ลงไฟล์"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(shots, f, ensure_ascii=False, indent=2)


# ---------- ส่วนที่ 2: ฟังก์ชันจัดการข้อมูล ----------

def next_id(shots):
    """หา id ถัดไป (ไม่ซ้ำกับของเดิม)"""
    if not shots:
        return 1
    return max(s["id"] for s in shots) + 1


def add_shot(shots):
    name = input("ชื่อ shot (เช่น SH010): ").strip()
    if not name:
        print("ชื่อห้ามว่าง")
        return
    task = input("ประเภทงาน (เช่น Roto / Matchmove / Paint): ").strip()
    assignee = input("ผู้รับผิดชอบ: ").strip()
    deadline = input("deadline (YYYY-MM-DD): ").strip()

    shot = {
        "id": next_id(shots),
        "name": name,
        "task": task,
        "assignee": assignee,
        "deadline": deadline,
        "status": "Todo",
    }
    shots.append(shot)
    save_shots(shots)
    print(f"เพิ่ม shot '{name}' แล้ว")


def list_shots(shots):
    if not shots:
        print("ยังไม่มี shot")
        return
    print(f"\n{'ID':<4}{'Shot':<12}{'Task':<12}{'Assignee':<12}{'Deadline':<12}Status")
    print("-" * 65)
    for s in shots:
        print(
            f"{s['id']:<4}{s['name']:<12}{s['task']:<12}"
            f"{s['assignee']:<12}{s['deadline']:<12}{s['status']}"
        )


def find_shot(shots, shot_id):
    """หา shot จาก id ถ้าไม่เจอคืน None"""
    for s in shots:
        if s["id"] == shot_id:
            return s
    return None


def ask_id():
    """ถาม id จากผู้ใช้ ถ้าไม่ใช่ตัวเลขคืน None"""
    text = input("ใส่ ID ของ shot: ").strip()
    if not text.isdigit():
        print("ID ต้องเป็นตัวเลข")
        return None
    return int(text)


def update_status(shots):
    shot_id = ask_id()
    if shot_id is None:
        return
    shot = find_shot(shots, shot_id)
    if shot is None:
        print("ไม่พบ shot นี้")
        return

    print("สถานะที่เลือกได้:")
    for i, status in enumerate(STATUSES, start=1):
        print(f"  {i}. {status}")
    choice = input("เลือกหมายเลข: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(STATUSES)):
        print("ตัวเลือกไม่ถูกต้อง")
        return

    shot["status"] = STATUSES[int(choice) - 1]
    save_shots(shots)
    print(f"เปลี่ยนสถานะเป็น {shot['status']} แล้ว")


def delete_shot(shots):
    shot_id = ask_id()
    if shot_id is None:
        return
    shot = find_shot(shots, shot_id)
    if shot is None:
        print("ไม่พบ shot นี้")
        return
    shots.remove(shot)
    save_shots(shots)
    print("ลบแล้ว")


# ---------- ส่วนที่ 3: เมนูหลัก ----------

def main():
    shots = load_shots()

    while True:
        print("\n=== VFX Shot Tracker ===")
        print("1. เพิ่ม shot")
        print("2. ดูรายการ shot")
        print("3. เปลี่ยนสถานะ")
        print("4. ลบ shot")
        print("0. ออก")
        choice = input("เลือกเมนู: ").strip()

        if choice == "1":
            add_shot(shots)
        elif choice == "2":
            list_shots(shots)
        elif choice == "3":
            update_status(shots)
        elif choice == "4":
            delete_shot(shots)
        elif choice == "0":
            print("ลาก่อน")
            break
        else:
            print("เมนูไม่ถูกต้อง")


if __name__ == "__main__":
    main()
    