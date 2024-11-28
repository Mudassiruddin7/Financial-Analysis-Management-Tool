![Fintech](https://media.tenor.com/tWLm4R_W3-MAAAAM/financial-advisor-jet760.gif)

# _**Financial Analysis & Management Tool**_

AI-driven solution designed to optimize financial management in high-transaction retail environments like DMart. It addresses key challenges such as scattered sales data, rising inventory costs, and high wastage rates by providing a unified platform for sales, inventory, and profitability analysis.

The tool integrates demand forecasting, wastage reduction, and financial optimization, offering real-time insights through interactive dashboards. With advanced ML models like Prophet and LSTM, it predicts future sales trends and suggests optimal inventory restocking levels.

# _**Base Paper**_

- https://www.researchgate.net/publication/350833314_A_Comprehensive_Financial_Analysis_Tools_on_the_Financial_Institution_on_COVID-19_Perspective
- https://www.researchgate.net/publication/23779178_Tools_of_Financial_Analysis
- https://www.raijmr.com/ijrsml/wp-content/uploads/2019/10/IJRSML_2017_vol05_sp.issue_2_Eng_24.pdf

# _**Algorithm Description**_

**Demand Forecasting:**
Demand forecasting is the process of making estimations about future customer demand over a defined period, using historical data and other information.

Usually organisations follow tranditional forecasting techniques/algorithms such as Auto Arima, Auto Arima, Sarima, Simple moving average and many more.

![RF](https://s32519.pcdn.co/wp-content/uploads/2024/05/fig1-ml-retail-forecasting-1024x508.png)

**Reference**

- https://www.geeksforgeeks.org/inventory-demand-forecasting-using-machine-learning-python/

# _**XGboost**_

XGBoost, or Extreme Gradient Boosting, is a machine learning algorithm designed for speed and performance. It builds many decision trees in sequence, where each new tree tries to correct the mistakes made by the previous ones. This process improves accuracy and helps in making better predictions. XGBoost is popular because it's fast, handles missing data well, and works great with large datasets. It's used in a variety of tasks like classification, regression, and ranking. Its efficiency and accuracy have made it a go-to choice for many data scientists and machine learning competitions.

![CNN](https://media.geeksforgeeks.org/wp-content/uploads/20210707140912/Bagging.png)

**K-Nearest Neigbour:**
KNN or K Nearest neighbours is a basic yet an efficient algorithm which is being used in most of the Machine learning application. Since it is a non-parametric i.e. This algorithm doesn’t make any underlying assumption like other algorithms do, such as having specify distribution of data to work with. So, this makes it very easy and understandable to all the users who are using it. The Technique KNN applies in predicting on new data is where it finds the nearest neighbours for the given point and takes a majority voting, whichever class is resided near to the new point, it will be considered as the new class for the new data point.

![KNN](https://static.javatpoint.com/tutorial/machine-learning/images/k-nearest-neighbor-algorithm-for-machine-learning2.png)

**Reference**

- https://www.geeksforgeeks.org/k-nearest-neighbours/
- https://www.ibm.com/topics/knn

# _**How to Execute?**_

So, before execution we have some pre-requisites that we need to download or install i.e., anaconda environment, python and a code editor.
**Anaconda**: Anaconda is like a package of libraries and offers a great deal of information which allows a data engineer to create multiple environments and install required libraries easy and neat.

**Download link:**

![Anaconda](https://1.bp.blogspot.com/-UJ1Ws2zZ9V4/TtMbG2ynJiI/AAAAAAAABbM/m6t2kuEhKdY/s1600/The-biggest-anaconda-snake-3.jpg)

https://www.anaconda.com/

**Python**: Python is a most popular interpreter programming language, which is used in almost every field. Its syntax is very similar to English language and even children and learning it nowadays, due to its readability and easy syntax and large community of users to help you whenever you face any issues.

**Download link:**

![Python](https://i0.wp.com/reptileworldfacts.com/wp-content/uploads/2019/05/male-blonde-super-tiger-reticulated-python.jpg?resize=351%2C351&ssl=1)

https://www.python.org/downloads/

**Code editor**: Code editor is like a notepad for a programming language which allows user to write, run and execute program which we have written. Along with these some code editors also allows us to debug, which usually allows users to execute the code line by line and allows them to see where and how to solve the errors. But I personally feel visual code is very good to work with any programming language and makes a great deal of attachment with user.

**Download links:**

![Vs code](https://schwabencode.com/contents/logos/VS2019-Badge.png) ![Pycharm](https://i0.wp.com/scracked.com/wp-content/uploads/2020/01/PyCharm-2019.3.4-Crack.png?fit=200%2C200&ssl=1)

- https://code.visualstudio.com/Download,
- https://www.jetbrains.com/pycharm/download/#section=windows

# _**How to create a new environment and configure jupyter notebook with it.**_

Let us define an environment and why we need different environments. An environment is a collection of libraries that are required to run our project. When we already have an environment with the necessary libraries, why do we need a new environment?
To avoid version mismatches, we create a new environment for each project. For example, in your previous project, you used "tf env" with tensorflow 2.4 and keras 2.4, but in your current project, you must use tensorflow 2.6 and keras 2.6. If you continue your project in the "tf env" environment, there will be a version mismatch and you will need to update tensorflow and keras, but this will cause problems with the previous project's execution. To avoid this, we create a new environment with tensorflow 2.6 and keras 2.6 and resume our project.

Let us now see how to create an environment in anaconda.

- Type “conda create –n <<name_of_your_env>>”
  example: conda create -n env
- It will ask to proceed with the environment location, type ‘y’ and press enter.
- When you press ‘y’, the environment will be created. To activate your environment type conda activate <<your_env_name>> . E.g., conda activate myenv.
- You can see that the environment got changed after conda activate myenv line. It changed from “base” to “myenv” which means you are now working in “myenv” environment.
- To install a library in your virtual environment type pip install <library_name>.
  e.g., pip install pandas
- Instead of installing libraries one by one you can even install by bunch, i.e., we have a txt file called requirements.tx which consists of all the libraries required to proceed with the project, so we can use it.
- so, before installing requirements.txt, make sure you are in the specific path where your requirements.txt is located, basically this file is located in the folder where our executable files are located, so we need to move to that directory by following command.
  **cd C:\folder_name**
- Here A -> drive, folder name -> path where your executable file is saved
- I go to that file path in anaconda using cd command

1. Go to drive where your project file is.
2. Go to the path of your project using cd <path>
3. Type pip install –r requirements.txt

- And all your required libraries will be downloaded and you can start your project.
- But if you want to use jupyter notebook on the new environment you have to set it up for the new environment.
- After you have installed all the libraries and created an environment, you need an editor to run the code, that is starting jupyter notebook, as soon as you enter jupyter notebook in the terminal you will definitely get this error. “Jupiter” is not recognized as an internal or external command.
  So, to solve it it we have 2 commands.

1. conda install –c conda-forge jupyterlab
2. conda install –c anaconda python
   Now you are ready to use jupyter on this environment and start with your project!

![thanks](https://media1.tenor.com/images/11ae4fcfc41bb9e66a0176fcfc38e695/tenor.gif?itemid=8486985)

# _**Steps to execute**_

**Note:** Make sure you have added path while installing the software’s.

1. Install the prerequisites/software’s required to execute the code.
2. Press windows key and type in anaconda prompt a terminal opens up.
3. Before executing the code, we need to create a specific environment which allows us to install the required libraries necessary for our project.
   • Type conda create -name “env_name”, e.g.: conda create -name project_1
   • Type conda activate “env_name, e.g.: conda activate project_1
4. Make sure you are in the correct path in your terminal, where you have saved your executable file/folder. E.g.: cd A:\project\AI\Completed\project_name, then press enter.
5. Install necessary libraries from requirements.txt file provided.
6. Run pip install -r requirements.txt or conda install requirements.txt (Requirements.txt is a text file consisting of all the necessary libraries required for executing this python file. If it gives any error while installing libraries, you might need to install them individually.)
7. Demand Forecasting.ipynb consists of all the data cleaning steps, which are necessary to build a clean and efficient pickle model.
8. Run app.py to see the results.

**Note:**Please follow the above sequence if you would like to execute and the files require good system requirements to run.

# _**Data Description**_

Dataset is already been provided in notebooks folder just open the respective files to download.

![Dataset](https://miro.medium.com/v2/resize:fit:1200/1*c8wR6BtKoF-kG5lqqcI7hA.gif)

# _**Issues Faced.**_

1. We might face an issue while installing specific libraries.
2. Make sure you have the latest version of python or 3.8, since sometimes it might cause version mismatch.
3. Adding path to environment variables in order to run python files and anaconda environment in code editor, specifically in visual studio code.

# _**Note:**_

**All the required data hasn't been provided over here. Please feel free to contact me for any issues.**

### _**Let’s Connect**_

<a href="https://linkedin.com/in/mudassiruddin21" target="blank"><img align="center" src="https://cdn.jsdelivr.net/npm/simple-icons@3.0.1/icons/linkedin.svg" alt="mudassiruddin21" height="30" width="40" /></a>

![Connect](https://media2.giphy.com/media/l1O6zvqu7O317887HF/source.gif)

# _**Yes, you now have more knowledge than yesterday, Keep Going.**_

![Happy](https://media.giphy.com/media/GK7grZYLG7cs0/giphy.gif)
# Financial-Analysis-Management-Tool
