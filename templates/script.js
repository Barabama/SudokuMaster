// 生成空表格
function blankTable(index) {
    var table = document.createElement("table");
    table.setAttribute("id", index)

    for (var i = 0; i < 9; i++) {
        var row = document.createElement("tr");

        for (var j = 0; j < 9; j++) {
            var cell = document.createElement("td");
            cell.textContent = "";
            row.appendChild(cell);
        }
        table.appendChild(row);
    }
    return table
}

// 绘制数独
function drawSudoku(index, sudoku) {
    var table = document.getElementById(index);

    for (var i = 0; i < table.rows.length; i++) {
        var row = table.rows[i];

        for (var j = 0; j < row.cells.length; j++) {
            var cell = row.cells[j]
            if (sudoku[i][j] != 0) cell.textContent = sudoku[i][j]
            else cell.textContent = "";
        }
    }
}


function generate() {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/generate");
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
            var sudokuData = JSON.parse(this.responseText);

            var answers = sudokuData["answers"];
            var problems = sudokuData["problems"];

            for (var i = 0; i < tableNum; i++) {
                var sudoku = problems[i];
                drawSudoku(i, sudoku)

            }
        }
    };

    var data = {
        "table_num": tableNum,
        "difficulty": document.getElementById("difficulty").value
    }
    xhr.send(JSON.stringify(data));
}

var tableNum = 9;
var tableContainer = document.getElementById("table-container")
tableContainer.innerHTML = "";   // 清空表格内容
for (var i = 0; i < tableNum; i++) {
    blank = blankTable(i)
    tableContainer.appendChild(blank)
}
