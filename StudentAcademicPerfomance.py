import heapq
from collections import deque

# Class to manage all aspects of a student academic information
class StudentAcademicSystem:
    def __init__(self):
        # Initialize core data structures
        self.students = {}  # Dictionary: student ID → student data
        self.attendance_log = deque()  # Queue to track student attendance
        self.submissions_list = None  # Singly linked list to track submissions
        self.departments_tree = {}  # Simulated tree structure: dept/year → list of student IDs
        self.id_bst = None  # Binary Search Tree (BST) for student ID lookup
        self.friendship_graph = {}  # Graph to model friendships (adjacency list)

    # Function to input multiple students and store their data
    def input_student_data(self):
        print("\n--- Student Data Input ---")
        while True:
            try:
                num_students = int(input("How many students would you like to add?: "))
                if num_students <= 0:
                    print("Please enter a positive number.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        for _ in range(num_students):
            print(f"\nEnter details for student {_ + 1}:")
            
            # Ensure student ID is unique
            while True:
                student_id = input("Student ID: ").strip()
                if student_id in self.students:
                    print("This ID already exists. Please enter a unique ID.")
                else:
                    break
            
            # Input personal information
            name = input("Name: ").strip()
            while True:
                try:
                    age = int(input("Age: "))
                    if age < 15 or age > 50:
                        print("Please enter a reasonable age (15-50).")
                        continue
                    break
                except ValueError:
                    print("Invalid input. Please enter a number for age.")
            course = input("Course: ").strip()
            department = input("Department/Year Level: ").strip()
            
            # Input subjects and grades
            while True:
                try:
                    num_subjects = int(input("How many subjects does the student have?: "))
                    if num_subjects <= 0:
                        print("Please enter a positive number.")
                        continue
                    break
                except ValueError:
                    print("Invalid input. Please enter a number.")

            grades = {}  # Dictionary for subjects and grades
            for i in range(1, num_subjects + 1):
                subject_name = input(f"Enter name for Subject {i}: ").strip()
                while True:
                    try:
                        grade = float(input(f"Enter grade for {subject_name} (1.0 to 5.0): "))
                        if grade < 0 or grade > 5.0:
                            print("Grade must be between 1.0 to 5.0.")
                            continue
                        grades[subject_name] = grade
                        break
                    except ValueError:
                        print("Invalid input. Please enter a number.")

            # Calculate average and pass/fail status
            average = sum(grades.values()) / len(grades)
            status = "Pass" if average <= 3.5 else "Fail"
            
            # Store in students dictionary
            self.students[student_id] = {
                'name': name,
                'age': age,
                'course': course,
                'grades': grades,
                'average': average,
                'status': status,
                'department': department
            }

            # Update all supporting structures
            self._update_data_structures(student_id, name, department, average)
        
        print("\nStudent data successfully added!")

    # Update attendance queue, linked list, tree, BST, and graph
    def _update_data_structures(self, student_id, name, department, average):
        # Enqueue attendance
        self.attendance_log.append((student_id, name))

        # Append to linked list (submission log)
        submission = {'student_id': student_id, 'name': name, 'timestamp': 'now'}
        if not self.submissions_list:
            self.submissions_list = {'data': submission, 'next': None}
        else:
            current = self.submissions_list
            while current['next']:
                current = current['next']
            current['next'] = {'data': submission, 'next': None}

        # Add student to department/year group (tree structure)
        if department not in self.departments_tree:
            self.departments_tree[department] = []
        self.departments_tree[department].append(student_id)

        # Insert student ID into BST
        self._add_to_bst(student_id)

        # Initialize empty friendship list
        if student_id not in self.friendship_graph:
            self.friendship_graph[student_id] = []

    # Binary Search Tree node class
    class BSTNode:
        def __init__(self, student_id):
            self.student_id = student_id
            self.left = None
            self.right = None

    # Wrapper for BST insertion
    def _add_to_bst(self, student_id):
        if not self.id_bst:
            self.id_bst = self.BSTNode(student_id)
        else:
            self._bst_insert(self.id_bst, student_id)

    # Recursive BST insert
    def _bst_insert(self, node, student_id):
        if student_id < node.student_id:
            if node.left is None:
                node.left = self.BSTNode(student_id)
            else:
                self._bst_insert(node.left, student_id)
        else:
            if node.right is None:
                node.right = self.BSTNode(student_id)
            else:
                self._bst_insert(node.right, student_id)

    # Recursive factorial function
    def factorial(self, n):
        if n == 0 or n == 1:
            return 1
        else:
            return n * self.factorial(n - 1)

    # Search for student by name (linear) or ID (BST)
    def search_student(self):
        print("\n--- Student Search ---")
        print("1. Search by name (linear search)")
        print("2. Search by ID (BST search)")
        choice = input("Enter your choice (1-2): ")
        
        if choice == '1':
            name = input("Enter student name to search: ").strip()
            found = False
            for student_id, data in self.students.items():
                if name.lower() in data['name'].lower():
                    self._display_student(student_id, data)
                    found = True
            if not found:
                print("No student found with that name.")
        elif choice == '2':
            student_id = input("Enter student ID to search: ").strip()
            if self._bst_search(self.id_bst, student_id):
                self._display_student(student_id, self.students[student_id])
            else:
                print("No student found with that ID.")
        else:
            print("Invalid choice.")

    # BST search function
    def _bst_search(self, node, student_id):
        if node is None:
            return False
        if node.student_id == student_id:
            return True
        elif student_id < node.student_id:
            return self._bst_search(node.left, student_id)
        else:
            return self._bst_search(node.right, student_id)

    # Sorting students by name or average
    def sort_students(self):
        print("\n--- Sorting Options ---")
        print("1. Sort by name (A-Z)")
        print("2. Sort by average grade (high to low)")
        choice = input("Enter your choice (1-2): ")
        
        if choice == '1':
            sorted_students = sorted(self.students.items(), key=lambda x: x[1]['name'])
        elif choice == '2':
            sorted_students = sorted(self.students.items(), key=lambda x: x[1]['average'], reverse=True)
        else:
            print("Invalid choice.")
            return
        
        print("\nSorted Students:")
        for student_id, data in sorted_students:
            self._display_student(student_id, data)

    # Attendance demo using queue
    def log_attendance(self):
        print("\n--- Attendance Log (Queue) ---")
        if not self.attendance_log:
            print("No attendance records yet.")
            return
        
        # Show first in queue
        student_id, name = self.attendance_log[0]
        print(f"ID: {student_id}, Name: {name}")
        
        confirm = input("Mark this student as present? (y/n): ")
        if confirm.lower() == 'y':
            present_student = self.attendance_log.popleft()
            print(f"{present_student[1]} marked present.")
        else:
            print("Attendance marking cancelled.")

    # Heap usage to display top 3 students
    def display_top_grades(self):
        print("\n--- Top 3 Grades ---")
        if len(self.students) < 3:
            print("Need at least 3 students to show top grades.")
            return
        
        grade_heap = []
        for student_id, data in self.students.items():
            heapq.heappush(grade_heap, (-data['average'], student_id))  # Use negative for max-heap
        
        print("Top 3 Students:")
        for i in range(3):
            if grade_heap:
                neg_avg, student_id = heapq.heappop(grade_heap)
                data = self.students[student_id]
                print(f"{i+1}. {data['name']} - Average: {data['average']:.2f} ({data['status']})")

    # Graph demo for managing friendships
    def manage_friendships(self):
        print("\n--- Friendship Management ---")
        if len(self.students) < 2:
            print("Need at least 2 students to manage friendships.")
            return
        
        print("1. Add friendship")
        print("2. View friendships")
        choice = input("Enter your choice (1-2): ")
        
        if choice == '1':
            # Show list of available students
            print("Available students:")
            for student_id in self.students:
                print(f"{student_id}: {self.students[student_id]['name']}")
            
            student1 = input("Enter first student ID: ").strip()
            student2 = input("Enter second student ID: ").strip()

            if student1 == student2:
                print("A student cannot be friends with themselves.")
                return
            
            if student1 not in self.students or student2 not in self.students:
                print("One or both student IDs are invalid.")
                return
            
            if student2 not in self.friendship_graph[student1]:
                self.friendship_graph[student1].append(student2)
                self.friendship_graph[student2].append(student1)
                print("Friendship added successfully!")
            else:
                print("These students are already friends.")
        
        elif choice == '2':
            print("\nFriendship Graph:")
            for student_id, friends in self.friendship_graph.items():
                friend_names = [self.students[f]['name'] for f in friends]
                print(f"{self.students[student_id]['name']} is friends with: {', '.join(friend_names) if friend_names else 'None'}")

    # Hash table access demo
    def hash_search(self):
        print("\n--- Quick Search by ID (Hashing) ---")
        student_id = input("Enter student ID: ").strip()
        if student_id in self.students:
            print("Student found via hash table lookup:")
            self._display_student(student_id, self.students[student_id])
        else:
            print("No student found with that ID.")

    # Display all students with summary
    def display_all_students(self):
        print("\n--- All Student Records ---")
        if not self.students:
            print("No student records available.")
            return

        # Find top performer
        top_performer_id = max(self.students.items(), key=lambda x: x[1]['average'])[0]
        
        for student_id, data in self.students.items():
            self._display_student(student_id, data, student_id == top_performer_id)
        
        print("\nSummary:")
        print(f"Total students: {len(self.students)}")
        print(f"Top performer: {self.students[top_performer_id]['name']} with average {self.students[top_performer_id]['average']:.2f}")

    # Helper function to show student details
    def _display_student(self, student_id, data, is_top=False):
        top_marker = " (TOP PERFORMER!)" if is_top else ""
        print(f"\nID: {student_id}{top_marker}")
        print(f"Name: {data['name']}")
        print(f"Age: {data['age']}")
        print(f"Course: {data['course']}")
        print(f"Department/Year: {data['department']}")
        print("Grades:", ", ".join(f"{subject}: {grade:.2f}" for subject, grade in data['grades'].items()))
        print(f"Average: {data['average']:.2f}")
        print(f"Status: {data['status']}")

    # Main menu for user interaction
    def main_menu(self):
        while True:
            print("\n=== Student Academic System ===")
            print("1. Input Student Data")
            print("2. Search for a Student")
            print("3. Sort Students")
            print("4. Attendance Log (Queue Demo)")
            print("5. Top 3 Grades (Heap Demo)")
            print("6. Manage Friendships (Graph Demo)")
            print("7. Quick Search by ID (Hashing Demo)")
            print("8. Display All Students")
            print("9. Calculate Factorial (Recursion Demo)")
            print("10. Exit")
            
            choice = input("Enter your choice (1-10): ")
            
            if choice == '1':
                self.input_student_data()
            elif choice == '2':
                self.search_student()
            elif choice == '3':
                self.sort_students()
            elif choice == '4':
                self.log_attendance()
            elif choice == '5':
                self.display_top_grades()
            elif choice == '6':
                self.manage_friendships()
            elif choice == '7':
                self.hash_search()
            elif choice == '8':
                self.display_all_students()
            elif choice == '9':
                try:
                    n = int(input("Enter a number to calculate factorial: "))
                    if n < 0:
                        print("Factorial is not defined for negative numbers.")
                    else:
                        print(f"{n}! = {self.factorial(n)}")
                except ValueError:
                    print("Invalid input. Please enter a non-negative integer.")
            elif choice == '10':
                print("Exiting the system. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

# Entry point
if __name__ == "__main__":
    system = StudentAcademicSystem()
    system.main_menu()
