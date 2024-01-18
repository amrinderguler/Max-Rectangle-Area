from typing import List, Tuple
from fastapi import FastAPI, HTTPException

def largest_rectangle(matrix: List[List[int]]) -> Tuple[int, int, int, int]:
    if not matrix or not matrix[0]:
        raise ValueError("Invalid matrix")

    rows, cols = len(matrix), len(matrix[0])
    max_area = 0
    max_num = None
    max_row = 0
    max_col = 0

    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] != -9:  # Skip already processed cells
                num = matrix[i][j]
                width = 0
                while j + width < cols and matrix[i][j + width] == num:
                    width += 1

                for k in range(i, rows):
                    if k < rows and matrix[k][j] != num:
                        break
                    height = k - i + 1  # Update height

                    # Update the width based on the minimum width encountered so far
                    width = min(width, len([1 for x in matrix[k][j:j+width] if x == num]))

                    area = width * height
                    if area > max_area and width != height:
                        max_area = area
                        max_num = num
                        max_row = i
                        max_col = j

    return max_num, max_area, max_row, max_col

app = FastAPI()

@app.post("/largest_rectangle")
async def calculate_largest_rectangle(matrix: List[List[int]]):
    try:
        result = largest_rectangle(matrix)
        return {
            "largest_rectangle": {
                "number": result[0],
                "area": result[1],
            }
        }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





