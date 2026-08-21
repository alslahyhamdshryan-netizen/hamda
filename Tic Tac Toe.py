import random
from tkinter import *


def next_turn(row, column):
    global player
    # التحقق من أن الخانة فارغة ولم ينتهِ الجيم بعد
    if buttons[row][column]["text"] == "" and check_winner() is False:
        buttons[row][column]["text"] = player

        # تلوين حرف اللاعب بلون مخصص للأناقة
        if player == "X":
            buttons[row][column].config(fg="#E74C3C")  # أحمر للـ X
        else:
            buttons[row][column].config(fg="#3498DB")  # أزرق للـ O

        winner_status = check_winner()

        if winner_status is True:
            label.config(text=(f"🎉 اللاعب {player} فاز!"), fg="#2ECC71")
            update_score(player)
            disable_all_buttons()
        elif winner_status == "Tie":
            label.config(text="🤝 تعادل!", fg="#F39C12")
            update_score("Tie")
        else:
            # تبديل الدور للاعب التالي
            player = players[1] if player == players[0] else players[0]
            label.config(text=f"دور اللاعب: {player}", fg="#34495E")


def check_winner():
    # فحص الصفوف
    for row in range(3):
        if (
            buttons[row][0]["text"]
            == buttons[row][1]["text"]
            == buttons[row][2]["text"]
            != ""
        ):
            highlight_winner(
                buttons[row][0], buttons[row][1], buttons[row][2]
            )
            return True

    # فحص الأعمدة
    for column in range(3):
        if (
            buttons[0][column]["text"]
            == buttons[1][column]["text"]
            == buttons[2][column]["text"]
            != ""
        ):
            highlight_winner(
                buttons[0][column], buttons[1][column], buttons[2][column]
            )
            return True

    # فحص القطر الرئيسي
    if (
        buttons[0][0]["text"]
        == buttons[1][1]["text"]
        == buttons[2][2]["text"]
        != ""
    ):
        highlight_winner(buttons[0][0], buttons[1][1], buttons[2][2])
        return True

    # فحص القطر الثانوي
    if (
        buttons[0][2]["text"]
        == buttons[1][1]["text"]
        == buttons[2][0]["text"]
        != ""
    ):
        highlight_winner(buttons[0][2], buttons[1][1], buttons[2][0])
        return True

    # فحص التعادل
    if empty_spaces() is False:
        for row in range(3):
            for column in range(3):
                buttons[row][column].config(bg="#BDC3C7", fg="#7F8C8D")
        return "Tie"

    return False


def highlight_winner(b1, b2, b3):
    """إضاءة الأزرار الفائزة وتعتيم البقية"""
    for row in range(3):
        for column in range(3):
            buttons[row][column].config(bg="#ECF0F1")

    # تلوين الأزرار الثلاثة الفائزة باللون الأخضر
    b1.config(bg="#2ECC71", fg="#FFFFFF")
    b2.config(bg="#2ECC71", fg="#FFFFFF")
    b3.config(bg="#2ECC71", fg="#FFFFFF")


def disable_all_buttons():
    """منع الضغط على الأزرار بعد انتهاء اللعبة"""
    for row in range(3):
        for column in range(3):
            if buttons[row][column]["text"] == "":
                buttons[row][column].config(state=DISABLED)


def empty_spaces():
    for row in range(3):
        for column in range(3):
            if buttons[row][column]["text"] == "":
                return True
    return False


def update_score(winner):
    global x_score, o_score, tie_score
    if winner == "X":
        x_score += 1
    elif winner == "O":
        o_score += 1
    elif winner == "Tie":
        tie_score += 1

    score_label.config(
        text=f" X: {x_score}  |  التعادلات: {tie_score}  |  O: {o_score} "
    )


def new_game():
    global player
    player = random.choice(players)
    label.config(text=f"دور اللاعب: {player}", fg="#34495E")

    for row in range(3):
        for column in range(3):
            buttons[row][column].config(
                text="", bg="#FFFFFF", state=NORMAL, fg="#000000"
            )


# إعداد النافذة الرئيسية والتصميم العام
wn = Tk()
wn.title("المطور ابن الصلاحي")
wn.configure(bg="#F5F7FA")  # خلفية هادئة ومريحة

players = ["X", "O"]
player = random.choice(players)

x_score = 0
o_score = 0
tie_score = 0

# عنوان اللعبة العلوي وطبقة الأدوار
label = Label(
    text=f"دور اللاعب: {player}", font=("Segoe UI", 24, "bold"), bg="#F5F7FA"
)
label.pack(pady=10)

# لوحة النتيجة (Scoreboard)
score_label = Label(
    text=f" X: 0  |  التعادلات: 0  |  O: 0 ",
    font=("Segoe UI", 14, "bold"),
    bg="#34495E",
    fg="#FFFFFF",
    padx=15,
    pady=5,
)
score_label.pack(pady=5)

# شبكة الأزرار للعب
frame = Frame(wn, bg="#F5F7FA")
frame.pack(pady=15)

buttons = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

for row in range(3):
    for column in range(3):
        buttons[row][column] = Button(
            frame,
            text="",
            font=("Segoe UI", 28, "bold"),
            width=5,
            height=2,
            bg="#FFFFFF",
            activebackground="#EAEDED",
            relief="groove",
            bd=2,
            command=lambda r=row, c=column: next_turn(r, c),
        )
        buttons[row][column].grid(row=row, column=column, padx=4, pady=4)

# زر إعادة التشغيل بتصميم عصري بالأسفل
reset_button = Button(
    text="جولة جديدة 🔄",
    font=("Segoe UI", 14, "bold"),
    bg="#2E4053",
    fg="white",
    activebackground="#34495E",
    activeforeground="white",
    bd=0,
    padx=20,
    pady=8,
    command=new_game,
)
reset_button.pack(side="bottom", pady=20)

wn.mainloop()