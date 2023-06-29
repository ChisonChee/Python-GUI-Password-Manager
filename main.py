from tkinter import messagebox
from tkinter import *
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def pw_generate():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []
    password_list += [random.choice(letters) for char in range(nr_letters)]
    password_list += [random.choice(symbols) for char in range(nr_symbols)]
    password_list += [random.choice(numbers) for char in range(nr_numbers)]

    random.shuffle(password_list)

    password = "".join(password_list)

    pw_entry.delete(0, END)
    pw_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_pw():
    website_name = website_entry.get().lower()
    id = id_entry.get()
    pw = pw_entry.get()
    data = {
        website_name: {
            "ID": id,
            "PW": pw
        }
    }

    if len(website_name) > 0 and len(id) > 0 and len(pw) > 0:
        is_ok = messagebox.askokcancel(title=website_name, message=f"ID: {id}\nPW: {pw}\nSave?")
        if is_ok:
            try:
                with open("./data.json", mode="r") as id_data:
                    history = json.load(id_data)
                    history.update(data)
            except FileNotFoundError:
                with open("./data.json", mode="w") as id_data:
                    json.dump(data, id_data, indent=4)
            except json.decoder.JSONDecodeError:
                with open("./data.json", mode="w") as id_data:
                    json.dump(data, id_data, indent=4)
            else:
                history.update(data)
                with open("./data.json", mode="w") as id_data:
                    json.dump(history, id_data, indent=4)

            finally:
                website_entry.delete(0, END)
                pw_entry.delete(0, END)
    else:
        messagebox.showerror(title="ERROR!", message="Hey! Don't leave any field empty!")


# ---------------------------- SEARCH MECHANISM ------------------------------- #
def search():
    try:
        with open("./data.json", mode="r") as data:
            data_dict = json.load(data)
            called_website = data_dict[f"{website_entry.get().lower()}"]
            called_id = called_website["ID"]
            called_pw = called_website["PW"]
    except FileNotFoundError:
        messagebox.showerror(title="Error!", message=f"Empty file. Please key in and add the website's USER_ID"
                                                     f" and PASSWORD")
    except KeyError:
        messagebox.showerror(title="Invalid info", message=f"No data found. Please key in the website "
                                                           f"or add the website's USER_ID and PASSWORD.")
    except json.decoder.JSONDecodeError:
        messagebox.showerror(title="Invalid info", message=f"Please key in and add the website's"
                                                           f" USER_ID and PASSWORD.")
    else:
        messagebox.showinfo(title=f"Website: {website_entry.get().lower()}", message=f"USER ID: {called_id}\nPASSWORD:"
                                                                                     f"{called_pw}\n"
                                                                        f"Press ctrl + v to paste the password")
        pyperclip.copy(called_pw)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.config(padx=20, pady=20, bg="white")

canvas = Canvas(width=200, height=200, bg="white", highlightthickness=0)
bg_img = PhotoImage(file="./logo.png")
canvas.create_image(100, 100, image=bg_img)
canvas.grid(column=1, row=0, padx=20, pady=20)

website = Label(text="Website:", font="times 15 bold", anchor="e", bg="white")
website.config(padx=10, pady=10)
website.grid(column=0, row=1)

website_entry = Entry(width=21, font="times 15 bold", bg="white", highlightthickness=1)
website_entry.grid(column=1, row=1, padx=10, pady=10)
website_entry.focus()

id_label = Label(text="User ID:", font="times 15 bold", anchor="e", bg="white")
id_label.config(padx=10, pady=10)
id_label.grid(column=0, row=2)

id_entry = Entry(width=35, font="times 15 bold", bg="white", highlightthickness=1)
id_entry.grid(column=1, row=2, columnspan=2, padx=10, pady=10)
id_entry.insert(0, "ChisonChee@gmail.com")

pw_label = Label(text="Password:", font="times 15 bold", anchor="e", bg="white")
pw_label.config(padx=10, pady=10)
pw_label.grid(column=0, row=3)

pw_entry = Entry(width=21, font="times 15 bold", bg="white", highlightthickness=1)
pw_entry.grid(column=1, row=3, pady=10, padx=10)

pw_generator = Button(text="Generate Password", font="times 9 bold", bg="white", highlightthickness=1,
                      command=pw_generate)
pw_generator.grid(column=2, row=3, pady=10, padx=10)

save_pw = Button(width=38, text="Add", font="times 12 bold", bg="white", highlightthickness=1, command=save_pw)
save_pw.grid(column=1, row=4, columnspan=3, pady=10, padx=10)

search_dat = Button(width=14, text="Search", font="times 9 bold", bg="white", highlightthickness=1, command=search)
search_dat.grid(row=1, column=2, padx=10, pady=10)

window.mainloop()
