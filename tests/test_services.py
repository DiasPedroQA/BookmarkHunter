# import os
# from app.services import analyze_path


# def test_analyze_path_file():
#     mock_file = "mock_file.txt"
#     with open(mock_file, "w") as f:
#         f.write("test")

#     result = analyze_path(mock_file)
#     assert result["exists"] is True
#     assert result["is_file"] is True
#     assert result["is_directory"] is False

#     os.remove(mock_file)


# def test_analyze_path_directory():
#     mock_dir = "mock_dir"
#     os.mkdir(mock_dir)

#     result = analyze_path(mock_dir)
#     assert result["exists"] is True
#     assert result["is_file"] is False
#     assert result["is_directory"] is True

#     os.rmdir(mock_dir)


# def test_analyze_path_invalid():
#     result = analyze_path("invalid_path")
#     assert result["exists"] is False
