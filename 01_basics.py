name = "kilosail"
age = 21
is_student = True

print(type(name))
print(type(age))
print(type(is_student))

languages = ["Python", "C#", "C++"]

print(languages)
print(languages[0])
print(languages[1])
print(languages[2])
languages.append("Java")
languages.remove("C#")
print(len(languages))

user = {
    "name": "kilosail",
    "age": 21,
    "role": "student"
}

print(user["name"])
print(user["age"])
print(user["role"])