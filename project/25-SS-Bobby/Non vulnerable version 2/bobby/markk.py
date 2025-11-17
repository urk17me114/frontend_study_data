from login.models import Marks, Subject, Student, ClassSection, TeacherAvailability
from datetime import date

# (marks, exam_type, exam_date, subject_name, student_username, class_section_id, teacher_username)
marks_data = [
    (60, 'Midterm', '2025-07-02', 'Art', 'CKC894', '6', 'FRQ386'),
    (68, 'Midterm', '2025-07-02', 'Art', 'CTY578', '6', 'FRQ386'),
    (71, 'Midterm', '2025-07-02', 'Art', 'FDC489', '6', 'FRQ386'),
    (50, 'Midterm', '2025-07-02', 'Art', 'HJR827', '6', 'FRQ386'),
    (90, 'Midterm', '2025-07-02', 'Art', 'HYT684', '6', 'FRQ386'),
    (74, 'Midterm', '2025-07-02', 'Art', 'KXR005', '6', 'FRQ386'),
    (88, 'Midterm', '2025-07-02', 'Art', 'LRG905', '6', 'FRQ386'),
    (31, 'Midterm', '2025-07-02', 'Art', 'PZC342', '6', 'FRQ386'),
    (93, 'Midterm', '2025-07-02', 'Art', 'RSB422', '6', 'FRQ386'),

    (90, 'Midterm', '2025-07-03', 'Math', 'CKC894', '6', 'HNV019'),
    (68, 'Midterm', '2025-07-03', 'Math', 'CTY578', '6', 'HNV019'),
    (85, 'Midterm', '2025-07-03', 'Math', 'FDC489', '6', 'HNV019'),
    (79, 'Midterm', '2025-07-03', 'Math', 'HJR827', '6', 'HNV019'),
    (90, 'Midterm', '2025-07-03', 'Math', 'HYT684', '6', 'HNV019'),
    (89, 'Midterm', '2025-07-03', 'Math', 'KXR005', '6', 'HNV019'),
    (88, 'Midterm', '2025-07-03', 'Math', 'LRG905', '6', 'HNV019'),
    (78, 'Midterm', '2025-07-03', 'Math', 'PZC342', '6', 'HNV019'),
    (67, 'Midterm', '2025-07-03', 'Math', 'RSB422', '6', 'HNV019'),

    (59, 'Midterm', '2025-07-01', 'Art', 'ALK414', '4', 'FRQ386'),
    (52, 'Midterm', '2025-07-01', 'Art', 'AWL724', '4', 'FRQ386'),
    (81, 'Midterm', '2025-07-01', 'Art', 'BAV516', '4', 'FRQ386'),
    (67, 'Midterm', '2025-07-01', 'Art', 'BFL908', '4', 'FRQ386'),
    (75, 'Midterm', '2025-07-01', 'Art', 'BWW409', '4', 'FRQ386'),
    (79, 'Midterm', '2025-07-01', 'Art', 'DOC136', '4', 'FRQ386'),
    (94, 'Midterm', '2025-07-01', 'Art', 'HAE147', '4', 'FRQ386'),
    (80, 'Midterm', '2025-07-01', 'Art', 'KQJ848', '4', 'FRQ386'),
    (82, 'Midterm', '2025-07-01', 'Art', 'LFN565', '4', 'FRQ386'),
    (48, 'Midterm', '2025-07-01', 'Art', 'MGM438', '4', 'FRQ386'),
    (92, 'Midterm', '2025-07-01', 'Art', 'VUP392', '4', 'FRQ386'),
    (74, 'Midterm', '2025-07-01', 'Art', 'WXL608', '4', 'FRQ386'),

    (63, 'Midterm', '2025-07-03', 'Art', 'EXR924', '5', 'FRQ386'),
    (26, 'Midterm', '2025-07-03', 'Art', 'HNE733', '5', 'FRQ386'),
    (85, 'Midterm', '2025-07-03', 'Art', 'LQH381', '5', 'FRQ386'),
    (45, 'Midterm', '2025-07-03', 'Art', 'PBF652', '5', 'FRQ386'),
    (46, 'Midterm', '2025-07-03', 'Art', 'QJO968', '5', 'FRQ386'),
    (76, 'Midterm', '2025-07-03', 'Art', 'QNT175', '5', 'FRQ386'),
    (91, 'Midterm', '2025-07-03', 'Art', 'QQB417', '5', 'FRQ386'),
    (85, 'Midterm', '2025-07-03', 'Art', 'QWS986', '5', 'FRQ386'),
    (73, 'Midterm', '2025-07-03', 'Art', 'VIN058', '5', 'FRQ386'),
    (76, 'Midterm', '2025-07-03', 'Art', 'YER334', '5', 'FRQ386'),
]

for mark, exam_type, exam_date, subject_name, student_username, class_section_id, teacher_username in marks_data:
    try:
        subject = Subject.objects.get(name=subject_name)
        student = Student.objects.get(username=student_username)
        class_section = ClassSection.objects.get(id=class_section_id)
        teacher = TeacherAvailability.objects.get(username=teacher_username)

        Marks.objects.create(
            username=student,
            subject=subject,
            class_section=class_section,
            marks=mark,
            exam_type=exam_type,
            exam_date=date.fromisoformat(exam_date),
            added_by=teacher
        )
    except Exception as e:
        print(f"Failed to insert mark for {student_username} ({subject_name}): {e}")

print("Marks insertion completed.")
