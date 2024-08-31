# musical-eureka

<details> 
    <summary><H1>Creating Venv</H1></summary>

1. Navigate to Your Project Directory: Open your terminal (or command prompt) and navigate to the directory where you want to create your project.
``` 
    cd path/to/your/project 
```
2. Run creating a .evn file replace name_venv with name that you think is suitable
```
    python3 -m venv name_venv
```
3. Activate the Virtual Environment:
```
    source venv/bin/activate
```
4. Incase if you are using .ipynb files then you need to follow some addition steps
    1. Set you python interpreter to the newly created vevn file bin/python3
    2. you can just copy paste the path to the file
    3. post that you may need to install ipykernel as well
    4. you can the select the interpreter from the to right corner 
</details>

<details> 
    <summary><H1>Create_venv.sh</H1></summary>
To save time you can use this shell script which will

1. Create a venv in the current working directory
2. Make sure you move the reuqired directory when you are run the given script
3. it will name the venv with the name of the folder you are working in
4. It will install this basic lib numpy pandas ipykernel
</details>