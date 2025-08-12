import pytest
from pydantic import ValidationError
from app.api.v1.schemas import Department, Course

class TestDepartmentSchema:
    """Test Department Pydantic model"""
    
    @pytest.mark.parametrize("missing_field", ["id", "name", "code"])
    def test_department_missing_required_fields(self, missing_field):
        """Test that a ValidationError is raised if a required field is missing."""
        valid_data = {
            "id": "cs",
            "name": "Computer Science",
            "code": "CS",
            "description": ""
        }
        
        # Remove the field for the current test case
        del valid_data[missing_field]

        with pytest.raises(ValidationError) as exc_info:
            Department(**valid_data) # type: ignore

        assert "Field required" in str(exc_info.value)

    def test_department_valid_data(self):
        """Test creating department with valid data"""
        dept = Department(
            id="cs",
            name="Computer Science and Engineering",
            code="CS",
            description=""
        )
        
        assert dept.id == "cs"
        assert dept.name == "Computer Science and Engineering"
        assert dept.code == "CS"
        assert dept.description == ""
    
    def test_department_invalid_code_format(self):
        """Test validation of department code format"""
        with pytest.raises(ValidationError):
            Department(
                id="cs",
                name="Computer Science",
                code="TOOLONG",
                description="CS Dept"
            )

    @pytest.mark.parametrize(
        "invalid_code, reason",
        [
            ("TOOLONG", "Too long (7 chars)"),
            ("A", "Too short (1 char)"),
            ("AB1", "Contains number"),
            ("Ab", "Contains lowercase"),
            ("aB", "Contains lowercase"),
            ("ab", "All lowercase"),
            ("A1", "Contains number"),
            ("1A", "Starts with number"),
            ("12", "All numbers"),
            ("A ", "Contains space"),
            ("A-B", "Contains hyphen"),
            ("A_B", "Contains underscore"),
            ("", "Empty string"),
            ("ABC", "Too long (3 chars)"),
            ("A@", "Contains special character"),
        ],
    )
    def test_department_invalid_code_format(self, invalid_code, reason):
        """Test validation of department code format"""
        with pytest.raises(ValidationError) as exc_info:
            Department(
                id="cs",
                name="Computer Science",
                code=invalid_code,
                description="CS Dept"
            )
        assert "code" in str(exc_info.value)
    
    @pytest.mark.parametrize("valid_code", ["CS", "EE", "ME", "CL", "AE", "MM"])
    def test_department_valid_code_format(self, valid_code):
        """Test that valid department codes pass validation"""
        dept = Department(
            id="test",
            name="Test Department",
            code=valid_code,
            description="Test"
        )
        assert dept.code == valid_code

class TestCourseSchema:
    """Test Course Pydantic model"""
    
    def test_course_valid_data(self):
        """Test creating course with valid data"""
        course = Course(
            id="cs101",
            course_name="Introduction to Programming",
            course_code="CS 101",
            course_type="Theory",
            slot="3"
        )
        
        assert course.course_code == "CS 101"
        assert course.course_type == "Theory"
        assert course.slot == "3"

    @pytest.mark.parametrize(
    "valid_code",
    [
        "CS 101",
        "EE 456",
        "ME2024",
        "CL8003",
    ],)
    def test_department_valid_code_format(self, valid_code):
        """Test that valid department codes pass validation."""
        try:
            Course(
                id="some_id",
                course_name="Some Name",
                course_code=valid_code,
                course_type="Theory",
                slot="3"
            )
        except ValidationError as e:
            pytest.fail(f"Validation failed unexpectedly for valid code '{valid_code}': {e}")
    
    @pytest.mark.parametrize(
    "invalid_code, reason",
    [
        ("CS123", "Too short (6 chars)"),
        ("CS 1234", "Too long (8 chars)"),
        ("TOLONG", "Too short, wrong format"),
        
        ("C1 123", "Prefix contains a number"),
        ("1234567", "Prefix is all numbers"),
        ("cs 123", "Prefix is lowercase"),
        
        ("CS 12A", "Suffix (with space) contains a letter"),
        ("CS ABCD", "Suffix (no space) contains letters"),
        ("CS 12", "Suffix (with space) is too short"),
        ("CS123", "Suffix (no space) is too short"),
        
        ("CS-123", "Contains a hyphen instead of space"),
        (" CS1234", "Starts with a space"),
        ("CS1234 ", "Ends with a space"),
    ],)
    def test_department_invalid_code_format(self, invalid_code, reason):
        """Test various invalid department code formats."""
        with pytest.raises(ValidationError) as exc_info:
            Course(
                id="test_id",
                course_name="Test Department",
                course_code=invalid_code,
                course_type="Theory",
                slot="3"
            )
        assert "course_code" in str(exc_info.value)

    @pytest.mark.parametrize("valid_course_type", ["Theory", "Lab"])
    def test_course_valid_course_type(self, valid_course_type):
        """Test that valid course types pass validation."""

        slot = "3" if valid_course_type == "Theory" else "L1"
        
        course = Course(
            id="cs101",
            course_name="Test Course",
            course_code="CS 101",
            course_type=valid_course_type,
            slot=slot
        )
        assert course.course_type == valid_course_type

    @pytest.mark.parametrize("invalid_course_type", ["Practical", "Lecture", "Tutorial", "theory", "lab", ""])
    def test_course_invalid_course_type(self, invalid_course_type):
        """Test validation of course course_type"""
        with pytest.raises(ValidationError):
            Course(
                id="cs101",
                course_name="Test Course",
                course_code="CS 101",
                course_type=invalid_course_type,  # Invalid course_type
                slot="3"  # Use Theory slot since we're testing course_type validation
            )

    @pytest.mark.parametrize("valid_slot", ["1", "5", "9", "10", "14"])
    def test_course_valid_slot_theory(self, valid_slot):
        """Test that valid slots pass validation for Theory courses."""
        course = Course(
            id="cs101",
            course_name="Test Course",
            course_code="CS 101",
            course_type="Theory",
            slot=valid_slot
        )
        assert course.slot == valid_slot

    @pytest.mark.parametrize("valid_slot", ["L1", "L3", "L6"])
    def test_course_valid_slot_lab(self, valid_slot):
        """Test that valid slots pass validation for Lab courses."""
        course = Course(
            id="cs101",
            course_name="Test Course",
            course_code="CS 101",
            course_type="Lab",
            slot=valid_slot
        )
        assert course.slot == valid_slot

    @pytest.mark.parametrize("invalid_slot", ["0", "15", "16", "L1", "L3", "L6", "A1", "B2", "l1", "1L", ""])
    def test_course_invalid_slot_theory(self, invalid_slot):
        """Test validation of invalid slots for Theory courses"""
        with pytest.raises(ValidationError):
            Course(
                id="cs101",
                course_name="Test Course",
                course_code="CS 101",
                course_type="Theory",
                slot=invalid_slot  # Invalid slot for Theory
            )

    @pytest.mark.parametrize("invalid_slot", ["1", "5", "14", "L0", "L7", "L10", "A1", "B2", "l1", "1L", ""])
    def test_course_invalid_slot_lab(self, invalid_slot):
        """Test validation of invalid slots for Lab courses"""
        with pytest.raises(ValidationError):
            Course(
                id="cs101",
                course_name="Test Course",
                course_code="CS 101",
                course_type="Lab",
                slot=invalid_slot  # Invalid slot for Lab
            )