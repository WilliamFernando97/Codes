{"metadata":{"kernelspec":{"display_name":"R","language":"R","name":"ir"},"language_info":{"mimetype":"text/x-r-source","name":"R","pygments_lexer":"r","version":"3.4.2","file_extension":".r","codemirror_mode":"r"}},"nbformat_minor":4,"nbformat":4,"cells":[{"cell_type":"code","source":"# %% [code]\n---\ntitle: \"Exploratory Data Analysis and Identifying riskiness of loan\"\noutput: html_document\n---\n\n* Introduction\n  + Dataset Overview\n  + Goal of the project\n  + Modelling  \n\n* Pre-Processing and Feauture selection\n  + Selecting variables\n  + load libraries\n  + Dealing with null values\n\n* Transformation and Inspecting variables\n  + Transformation of Job type, Savings.account,Purpose predictors \n  + Exploring transformation\n  + Transformation of countinous variables and eda\n  + Multivariate Transformation and Inspection\n  + Checking Multicolinearity\n  + Summary and Findings\n\n* Model \n  + Introduction of model\n  + Fitting logistic Regression Model\n  + Analyzing result \n    * Interpretation of coefficents\n    * Evaluating Model Perfomance \n    * Improving Model perfomance by balancing the target variable\n   \n* Summary and Conclusion\n    \n## 1.Introduction and Context  \n\n**Data**: My [dataset](https://www.kaggle.com/uciml/german-credit/kernels) contains information about 1000 german individual and their credit line and loans,including nine different parameters like age, sex, job, housing etc.Each row represent a person who has taken a loan. \n\n**Goal**: By using nine different parameters given in the dataset, we try to indentify riskiness of a loan and classified them into gooad and bad.Here, I am trying to explain how given parameters affecting riskiness of loan. \n\n   * Good Loan: It is a good investment from bank perspective and more likely recover the                  loan. \n   * Bad Loan: It is a bad investment from bank perpective and less likely to recover the                 loan, more chances of default.\n\nThus, it is utmost important to identify a loan correctly, if we identify a good loan as bad loan turns into business loss. on the other hand, if we identify a bad loan as a good loan turns into financial distress. \n\n**Modelling**: I will bulid logistic regression and evaluate the risks associated with other parameters while lending money to a loan applicant. We are trying to optimised result and helping a bank to set the decision parameters in identifying loan is a good or bad investment. \n\n*\n### Important Note:\n\nWhen I built the model by using the original dataset, the ratio of precision and recall was too law. It means the model was falsely identifying bad loan as a good loan. In business terms, we build the model to maximize profit and to minimize loss. However, here the classification made by the model would increase the risk of bad debt; eventually, it will convert in a financial loss for a bank.\n\nThe reason is why model predicting bad loan as a good because the ratio of good loan to the bad loan was 70:30. The values of the good loan were far higher than a bad loan in the target variable because of this reason I found the model was giving biased output and inclined towards the values of a good loan.\n\nTo overcome this imbalanced data, I used sampling method which modify the data into balanced distribution. In this analysis, I applied the oversampling method to balance minority class in the target variable.  \n\n\n## 2.Pre-Processing and Feauture selection\n\n*\n#### Selecting variables \n\nHere risk is a dependent variable and other nine variable those are explonatary varible helps us to understand riskiness while lending a loan to customers.\n\n* **Risk**:The variable we are trying to explain called as response variable.\n* **Age**:Borrower's age in years  \n* **Sex**:Borrower's sex(male or female) \n* **Job**:Types of Job    \n* **Housing**:  Borrower's housing type\n* **Saving accounts**:Type of savings account that shows tendency of borrowers for \nsaving\n* **Checking account**:Balance in checking account(Currency:DM - Deutsch Mark)\n* **Credit amount**:Credit line used by account holder.\n* **Duration**:loan duration in months \n* **Purpose**:Purpose of loan \n\n\n```{r}\n#load data\n\ndata <- read.csv(\"../input/orginaldata/germanCreditRisk_originalData.csv\")\n\n```\n\n```{r,echo=TRUE,message=FALSE,warning=FALSE}\n#load library\nlibrary(ROSE)\nlibrary(tidyverse)\nlibrary(gridExtra)\nlibrary(plyr)\nlibrary(knitr)\nlibrary(caret)\nlibrary(caTools)\nlibrary(DMwR)\n```\n\n```{r}\n# Checking basic structure and dimension of the dataset\n\ndim(data)\nstr(data)\n\n```\n\n\n* Some of the variables type need to be transform for better analysis and comparison.\nFirst variable **X** is just a serial number, we can get rid of the serial number.\n\n```{r}\n\ndata$X <- NULL\n\n```\n\n\n\n```{r}\n#Taking care of missing data\n\nsapply(data, function(x) sum(is.na(x)))\n\n```\n\n```{r}\n#Replacing Null Values with mode\n\ndata$Saving.accounts[is.na(data$Saving.accounts)]=\n  names(table(data$Saving.accounts))[table(data$Saving.accounts)==max(table(data$Saving.accounts))]\n\n\ndata$Checking.account[is.na(data$Checking.account)]=\n  names(table(data$Checking.account))[table(data$Checking.account)==max(table(data$Checking.account))]\n\n```\n\n## 3.Transformation and Inspecting variables\n\n*\n#### Transformation of Job type, Savings.account,Purpose predictors  \n\n```{r}\n\ndata$Job=as.factor(data$Job)\ntable(data$Job)\ntable(data$Saving.accounts)\ntable(data$Purpose)\n\n#Job Type\n\ndata$Job <- mapvalues(data$Job,from =c(\"0\",\"1\",\"2\",\"3\"),\n                      to = c(\"Unskilled\",\"Unskilled\",\"Skilled\",\"Highly Skilled\"))\n\n#Type of Savings.account\n\ndata$Saving.accounts <- mapvalues(data$Saving.accounts,from =c(\"little\",\"moderate\",\"quite rich\",\"rich\"), to = c(\"little\",\"moderate\",\"moderate\",\"moderate\"))\n\n#Purpose of the loan\n\ndata$Purpose <- mapvalues(data$Purpose,from = c(\"business\",\"car\",\"domestic appliances\",\n                \"education\",\"furniture/equipment\",\"radio/TV\",\"repairs\",\"vacation/others\"), \n                to = c(\"business\",\"car\",\"furniture/equipment\",\"education\",\n                       \"furniture/equipment\",\"radio/TV\",\"others\",\"others\")) \n\n```\n\n*\n#### Exploring Transformation\n\n```{r}\ng3 <- ggplot(data,aes(x=Job,fill = Job)) +\n  geom_bar()+\n  ggtitle(\"Type of Jobs\")+\ntheme_bw()+\n      theme(axis.text = element_text(size=12,face = \"bold\"),\n            legend.text = element_text(size = 12),\n            axis.title.x = element_blank(),\n            axis.title.y = element_blank(),\n            panel.grid.major = element_blank(),\n            panel.grid.minor = element_blank(),\n            panel.border = element_blank(),\n            axis.line = element_line(colour = \"black\")) +\n  theme(legend.position=\"bottom\")\n  \ntable(data$Saving.accounts)\n\n\ng4 <- ggplot(data,aes(x=Saving.accounts,fill=Saving.accounts))+\n  geom_bar()+\n  ggtitle(\"Types of savings account\")+\n  theme_bw()+\n      theme(axis.text = element_text(size=12,face = \"bold\"),\n            legend.text = element_text(size = 12),\n            axis.title.x = element_blank(),\n            axis.title.y = element_blank(),\n            panel.grid.major = element_blank(),\n            panel.grid.minor = element_blank(),\n            panel.border = element_blank(),\n            axis.line = element_line(colour = \"black\")) +\n  theme(legend.position=\"bottom\")\n\n grid.arrange(g3, g4, nrow=1)\n\n  \n\n```\n\n```{r}\n\ndata_filter<- data.frame(table(data$Purpose))\nnames(data_filter)=c(\"Purpose\",\"counts\")\nggplot(data_filter)+geom_bar(aes(x=reorder(Purpose,+counts),y= counts,fill = Purpose), stat=\"identity\")+ xlab(\"\")+ ylab(\"\")+ ggtitle(\"\")+ theme(legend.position = \"none\",axis.text = element_text(face = \"bold\"),plot.title = element_text(colour = \"darkorange\",face = \"bold\"))+\n  coord_flip() \n\n```\n\n```Job```\n\nThere was sparse level in Job Types. So I grouped category and convert into two category Skilled and Unskilled. \n\n```savings.account```\n\nI transformed all the four variable of savings.account to get a more clear understanding of the underlying scenario. Little was more when compared to other three. Hence, I merged other three variable and compared it to little to understand the pattern.\n\n```Purpose of loan```\n\nThere were a sparse value in this variable, category repairs and other/vacation was having less amount of example. So, I grouped them into single category named others. \n\n* Observation\n  + People who are skilled and highly skilled tend to apply more for credit.\n  + By analysing Checking.account, most of the client having little amount of wealth.\n  + People are more likely to apply for two basic reason to buy car and radio/tv. \n\n\n*\n#### Transformation of  Countinous Variables and eda\n\nThare was two countinous variables and I inspect by creating histogram to check skewness in variable.\n\n```{r}\ng1 <-  ggplot(data,aes(x = Age)) + \n  geom_histogram(bins = 20, fill = 'blue', colour = 'black') + \n  ggtitle('Age Distribution') + \n  xlab('Age') +\n  ylab('Frequency')\n\ng2 <- ggplot(data,aes(x = Credit.amount)) + \n  geom_histogram(bins = 20, fill = 'red', colour = 'black') + \n  ggtitle('Credit_Amount Distribution') + \n  xlab('Credit_Amount') +\n  ylab('Frequency')\n\ngrid.arrange(g1, g2, nrow=1)\n\n\n```\n\n* Observation:\n\nWe can see both ```Age``` and ```Credit_Amount``` are right skewed.So, I used ```log1p``` function to transform skewness in normal distribution.\n\n\n```{r}\n#Transforming variables\n\ng1 <-  ggplot(data,aes(x = log1p(Age))) + \n  geom_histogram(bins = 20, fill = 'blue', colour = 'black') + \n  ggtitle('Age Distribution') + \n  xlab('Age') +\n  ylab('Frequency')\n\ng2 <- ggplot(data,aes(x = log1p(Credit.amount))) + \n  geom_histogram(bins = 20, fill = 'red', colour = 'black') + \n  ggtitle('Credit_Amount Distribution') + \n  xlab('Credit_Amount') +\n  ylab('Frequency')\n\ngrid.arrange(g1, g2, nrow=1)\n\n\n```\n\n**Age**\n\nLog transformation of age helps to improve our distributon. ```Age``` variable is still slightly right skew;however it is much better distribution than eralier.\n\n*\n#### Multivariate Transformation and Inspection \n\n##### Dependent ~ Independent relationship\n\n##### Gender vs Credit.Amount\n\n```{r}\n\nggplot(data, aes(x=log1p(Credit.amount), fill=Sex)) +\n  geom_density(alpha=0.5) +\n  ggtitle('Distribution of Credit.amount by Gender') +\n  xlab(\"Credit.Amount\") + \n  ylab(\"Density\") \n\n```\n\n* Observation\n  + There is good assosiation between male and female loan application, but female             applicant getting slightly higher credit than male. \n\n```{r}\nggplot(data,aes(x=Risk, fill=Sex)) +\n  geom_bar(position='dodge') + \n  ggtitle(\"Proportion of Good and Bad loan by Sex\")+ \n  \n      theme_bw()+\n      theme(axis.text = element_text(size=12,face = \"bold\"),\n            legend.text = element_text(size = 12),\n            axis.title.x = element_blank(),\n            axis.title.y = element_blank(),\n            panel.grid.major = element_blank(),\n            panel.grid.minor = element_blank(),\n            panel.border = element_blank(),\n            axis.line = element_line(colour = \"black\"))\n \n\n```\n\n* Observation\n  + The number of male applicant almost double than female.\n  + The more risk assosicated with female loan applicant. \n\n```{r}\nggplot(data, aes(x=Purpose, y=Credit.amount, fill=Purpose)) +\n  geom_boxplot() + coord_flip()\n\n```\n\n* I created age group to inspect more, we can analyze which group applied more for loan and which group carrying more riskiness.\n\n```{r}\n# Categorical age\n\ndata <- data %>% mutate(\n  AgeCategories = case_when(\n    Age >= 18 & Age < 35 ~ 'Young adult',\n    Age >= 35 & Age < 60 ~ 'Middle Aged',\n    Age >= 60 ~ 'Elderly',\n    TRUE ~ as.character(NA)\n  )\n)\ndata$AgeCategories %>% table(useNA='always')\n\n```\n\n\n```{r}\n\n ggplot(data, aes(x=AgeCategories, y=Credit.amount, fill=AgeCategories)) +\n geom_bar(stat=\"identity\")+\n theme_minimal()+\n scale_fill_brewer(palette=\"Blues\")+\n ggtitle(\"Credit_Amount age group \")+\n theme(legend.position=\"none\")+\n theme_bw()+\n theme(axis.text = element_text(size=12,face = \"bold\"),\n            legend.text = element_text(size = 12),\n            axis.title.x = element_blank(),\n            axis.title.y = element_blank(),\n            panel.grid.major = element_blank(),\n            panel.grid.minor = element_blank(),\n            panel.border = element_blank(),\n            axis.line = element_line(colour = \"black\"))\n```\n\n* Observation\n  + People who fall between age 18 to 35 are applying more for loan will have to inspect       the riskiness associated with this group. It is also intresting to know why this           group is applying for more credit.\n\n```{r}\n\ntable(data$Housing)\n\na1 <- ggplot(data,aes(x=Risk, fill=Housing)) +\n  geom_bar(position='dodge') + \n  ggtitle(\"Loan Risk by housing type\")+ \n  \n      theme_bw()+\n      theme(axis.text = element_text(size=12,face = \"bold\"),\n            legend.text = element_text(size = 12),\n            axis.title.x = element_blank(),\n            axis.title.y = element_blank(),\n            panel.grid.major = element_blank(),\n            panel.grid.minor = element_blank(),\n            panel.border = element_blank(),\n            axis.line = element_line(colour = \"black\")) +\n  theme(legend.position=\"bottom\")\n\n   \na2<- ggplot(data,aes(x=Risk, fill=Saving.accounts)) +\n  geom_bar(position='dodge') + \n  ggtitle(\"Loan Risk by Savings.account\")+ \n  \n      theme_bw()+\n      theme(axis.text = element_text(size=12,face = \"bold\"),\n            legend.text = element_text(size = 12),\n            axis.title.x = element_blank(),\n            axis.title.y = element_blank(),\n            panel.grid.major = element_blank(),\n            panel.grid.minor = element_blank(),\n            panel.border = element_blank(),\n            axis.line = element_line(colour = \"black\")) +\n  theme(legend.position=\"bottom\")\n\n     \n\ngrid.arrange(a1,a2,nrow=1)\n\n\n\n```\n\n* Observation\n  + There is more probabolity of considering loan being risk for people who are having less     amount is savings account.\n  + The good things about bank most of the client own the house.We can clearly notice that     the proportion of people who own the house is significantly higher than other two          groups. \n\n\n*\n#### Checking Correlation between countinous variables(Multicolinearity)\n\n```{r,warning=FALSE,message=FALSE}\n\ndata <- data %>% mutate(LogAge = log(Age),\n                    Log1pCredit.amount = log1p(Credit.amount))\n\nprint(cor(data$LogAge,data$Log1pCredit.amount))\n\np1 <- ggplot(data,aes(x=LogAge, y=Log1pCredit.amount)) +\n  geom_point(colour = \"red\") +\n  geom_smooth(method='lm') + \n  ggtitle('Age vs Credit.amount') + \n  xlab('Age') +\n  ylab('Credit.amount')\n\nprint(cor(data$Log1pCredit.amount, data$Duration))\n\np2 <- ggplot(data,aes(x=Log1pCredit.amount, y= Duration)) +\n  geom_point(colour = \"red\") +\n  geom_smooth(method='lm') + \n  ggtitle('Duration vs Age') + \n  xlab('Duartion') +\n  ylab('Credit.amount')\n\nprint(cor(data$Duration, data$LogAge))\n\np3 <- ggplot(data,aes(x=Duration, y=LogAge)) +\n  geom_point(colour = \"red\") +\n  geom_smooth(method='lm') + \n  ggtitle('Duration vs Age') + \n  xlab('Duartion') +\n  ylab('Credit.amount')\n\ngrid.arrange(p1,p2,p3,nrow = 1)\n\n```\n\n* Observation\n  + To inspect multicolinearity between countinous variable in the data as presence of         multicolinearity disorts the standard error of coefficent and leadig to problem for        conducting t-test.\n  + There was no significant correlation between countinous variable.\n\n*\n#### Summary\n\n  * No multicolinearity\n  * Highest distribution of credit amount to car,radio/tv and equipment.\n  * More risk factor associated with female client than male.\n  * We should inspect the reasons why particular age group appilyng for more credit.\n  * Housing type and client has correlation with riskiness of loan.\n\n\n## 4.Modeling\n\nI am building a logistic regression model to predict the riskiness of the loan. Many elements in the dataset would help to identify the characteristic of the risk part resides in the loan. The proportion of good credit to the bad loan was 70%, we can say that there 30% chances of the default or it will probably create financial distress for the bank.\n\nI will run baseline model to check how independent variable helping to identify the loan being good or bad. After reading the result of the coefficient of variation, we will decide which variable to keep and which variable to exclude from our analysis.\n\n```{r}\ndata$LogAgestd <- scale(data$LogAge)\ndata$Log1pCredit.amountstd <- scale(data$Log1pCredit.amount)\n\n```\n\n* To make comparison better and accurate, I scaled logged value.Scaling basically normalizing tha data distribute in aparticular range will speep up algoritham perfomance. \n\n*\n#### Fitting Logistic Regression \n\n```{r}\n\nclassifier = glm(formula = Risk ~                  Age+Sex+Job+Housing+Saving.accounts+Checking.account+Duration+Purpose+LogAgestd+Log1pCredit.amountstd,family = binomial,data = data)\n\nsummary(classifier)\n\n```\n\n* Observation\n\nThere are many variables which did not helping to identify the riskiness in the loan. Simply, we can exclude all those variable which are not significant. We will only keep Savings.account, Checking.account, Duration and Housing as independent variable to predict the riskiness. Before, splitting the dataset into train and test, it would be better to understand the statistical significant of coefficient.\n\n*\n#### Interpreting coefficients\n\n```{r}\n# Exponentiated logistic regression coefficients\n\nclassifier %>% coefficients %>% exp %>% round(3)\n```\n\n* I run the exponential function to interpret percentage variation of particular predictor in our dataset and how well it contributing in explaining it effects in the model. (I am only explaining those coefficient which looks significant for our model )\n\n```Savings.accounts```: The odds of loan being good 100*(1.659 - 1) = 65.9% higher if the client maintain sufficient amount in their saving account. There are two types of savings account in Saving.account variable, but model converted the independent varaiable Saving.account into moderateSavingaccount, it means model picking moderateSaving account as baseline and converted into dummy variable. We can interpret that if saving account classify as little it would increase hazard rate for loan default by 34.1%.\n\n```Duration```: The odds of loan being good 100*(1-956)=4.4% less if the duration of the loan is longer. \n\n```Checking.account```: Bank classifying checking account into little, moderate and rich. The model converting little and moderate accounts into moderate and making it dummy variable for prediction. The odds of loan being good (1-0.615)=38.5% less if classify as moderate account. On the other side if the account classify as rich it will increasing probability of loan being good and reduce financial burden by 100*(1.085 - 1) = 8.5%.\n\n```Housing```: Housing variable converted into dummy variable. We can notice from the estimate that the person who owns the house has positive correlation with loan quality. When person owns the house it increase probability of loan being good by 100*(1.62-1)=62%.     \n\n\n```{r}\n\ncleanData <- read.csv(\"../input/creditriskanalysis/cleanData.csv\")\n\n```\n\n\n\n\n*\n#### Evaluating predictive performance\n\nI split the data into training and test to check the validity of the model more accurately. I saved the data on which I perform featuring engineering earlier as filename.csv to avoid transformation process again into train and test data\n\n```{r}\n# Splitting the dataset into training and test\n\nset.seed(123)\n\nsplit = sample.split(cleanData$Risk,SplitRatio = 0.80)\ntraining_set = subset(cleanData,split == TRUE)\ntest_set = subset(cleanData,split == FALSE)\n\n\n#Fitting the logistic regression into training_set\n\n\nclassifier1 = glm(formula = Risk ~ Duration + Housing + Saving.accounts + Checking.account, family = binomial(\"logit\"),data = training_set)\n\n#Predicting train result \nprob_pred = predict(classifier1,type = 'response',newdata = training_set[-11])\ny_pred1 = ifelse(prob_pred > 0.5,\"good\",\"bad\")\n\n#Predicting test result \nprob_pred = predict(classifier1,type = 'response',newdata = test_set[-11])\ny_pred2 = ifelse(prob_pred > 0.5,\"good\",\"bad\")\n\ncm1 = table(training_set[,11], y_pred1)\ncm1\n\ncm2 = table(test_set[,11], y_pred2)\ncm2\n\n```\n\n```{r}\n#Confusion matrix\n\ncm1 = table(training_set[,11], y_pred1)\ncm1\n\ncm2 = table(test_set[,11], y_pred2)\ncm2\n\n\n```\n\n```{r}\n\n#Calculating accuracy, precision and recall(train)\n\naccuracytrain = (44+527) / 800\nprecisiontrain = 44 / 240\nrecalltrain = 44/77\n\naccuracytrain\nprecisiontrain\nrecalltrain\n\n#Calculating accuracy, precision and recall(test)\n\naccuracytest = (10+133) / 200\nprecisiontest = 10 / 60\nrecalltest = 7/17\n\naccuracytest\nprecisiontest\nrecalltest\n\n\n\n\n\n```\n\n\n**Accuracy**: The accuracy of the model is similar in the both training and test dataset, approx. 71% of the time model classifying loan coreectly in both the set.\n\n**Precision**: When the model predicts loan being good or bad, it is only correctly identify 16.67% of the time.(type 2 error)\n\n**Recall**:The model approx. 41.17% of the time classify the loan being risky for the bank.\n\n\n*\n#### Summary \n\nI created baseline model to predict riskiness of the loan and probabilities of default. This model will help bank to determine which applicants should be accepted for loan and which applicants should not be.\n\n* Interpretation\n  + Prediction : The precision ratio is very low and alarming that model could not identifying bad loan correctly. When we compare accuracy with precision and recall the result seems different and it fails to explain the accuracy in the model.. We can consider as it type 2 error as the model fails to identify the bad loan as bad when it is actually bad. The other reason could be possible why model bias towards good loan, the proportion of good loan to bad loan was 70% in the original dataset. It might be possible that more values classified as good so more favourable towards it. \n\nThere are lot of categorical variable in the dataset, to improve model performance we must check collinearity in the categorical variable.We can also use other classification model to make prediction accurate like KNN or Random Forest Classification model.\n\n*\n#### Improving model perfomance by balancing traget variable\n\n```{r}\nsmote <- read.csv(\"../input/creditriskanalysis/cleanData.csv\")\n\n```\n\n\n```{r}\nsmotedata <- SMOTE(Risk ~ ., smote,prec.over = 400, k = 5 )\n```\n\n```{r}\n\nsmoteclassifier = glm(formula = Risk ~ Age+Sex+Job+Housing+Saving.accounts+Checking.account+Duration+Purpose+LogAgestd+Log1pCredit.amountstd,family = binomial,data =smotedata)\n\n```\n\n\n```{r}\nset.seed(300)\n\nsplit = sample.split(smotedata,SplitRatio = 0.80)\ntraining_smote = subset(smotedata,split == TRUE)\ntest_smote = subset(smotedata,split == FALSE)\n\n\n\nclassifier5 = glm(formula = Risk ~ Sex + Job +  Housing + Checking.account + Duration  ,family = binomial,data =smotedata)\n\n\n#Predicting train result \npred1 = predict(classifier5,type = 'response',newdata = training_smote[-11])\ny_predsmote = ifelse(pred1 > 0.5,\"good\",\"bad\")\n\n#Predicting test result \npred2 = predict(classifier5,type = 'response',newdata = test_smote[-11])\ny_predsmote1 = ifelse(pred2 > 0.50,\"good\",\"bad\")\n\ncmsmote1 = table(training_smote[,11], y_predsmote)\ncmsmote1\n\ncmsmote = table(test_smote[,11], y_predsmote1)\ncmsmote\n\n```\n\n```{r}\n#Calculating accuracy, precision and recall(train)\n\naccuracysmotetrain = (348+741) / 1575\nprecisionsmotetrain = 348 / 675\nrecallsmotetrain = 348/687\n\naccuracysmotetrain\nprecisionsmotetrain\nrecallsmotetrain\n\n#Calculating accuracy, precision and recall(test)\n\naccuracytsmoeteest = (118+238) / 525\nprecisionsmoetetest = 118 / 225\nrecallsmotetest = 118/180\n\naccuracytsmoeteest\nprecisionsmoetetest\nrecallsmotetest\n\n```\n\n**Accuracy**: The accuracy of the model is approximately similar in the both training and test dataset, approx. 68% of the time model classifying loan coreectly in both the set.\n\n**Precision**: When the model predicts loan being good or bad, it is correctly identify 52.44% of the time, which is good improvemrnt then earlier prediction.\n\n**Recall**:The model approx. 65.55% of the time classify the loan being risky for the bank.\n\n\n## 5.Summary and Conclusion \n\n* Analysis\n  + To improve model perfomance, I used sampling methods and oversampled the data to balance the distrubution of minorty class in the target variable. By doing oversampling, the model is giving more accurate output and increase the ratio of precision(65.55%) and \nrecall(52.44%). The precision has increased by almost 45%, which I think is a good improvement in predictive model.\n  + We performed detail explonatory data analysis on different categorical as well as countinous variable. By doing EDA we found sparse values in the variables and removed sparsity in all variables to analyse and measure accurate variation of all these independent variables on the target variables.\n  + Important skills, I have learnt drom this projects are following.\n    \n    1. Interpretation of coeffiecint \n    2. Standardizing of log transform values makes more sense in interpretation\n    3. How imbalanced data could make difference in prediction \n    4. How logistic regression converting categorical variables into dummy variables while there more than one subcategory in the predictor.\n    \n  + I would like to explore multivariate data analysis to know more precise relation between variables and how they are explaining target variables. For instance, there serval puropses for people had taken a loan. How different housing type of checking.account and savings.account explaning target variable.  ","metadata":{"_uuid":"ca1219f7-3bb9-4cb7-98a6-3e2209b8b646","_cell_guid":"e01da9f5-04a5-4ede-868b-4b93871ece02","collapsed":false,"jupyter":{"outputs_hidden":false},"trusted":true},"execution_count":null,"outputs":[]}]}