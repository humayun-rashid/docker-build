import os
loginSuccess = False
userPushSelection = str(input("Select from the options. \n 1. Create image 2. Create and Push image 3. Image List"))

def checkDockerInfo():
    files = []
    path = str(input("Type service directory. default is current directory ( ./ ). Press enter for default"))
    
    if path == "":
        path = "./"

    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if 'dockerfile' in file:
                files.append(os.path.join(r, file))
    
    if './dockerfile' in files:
        print('Docker config is found')
        return True
    
    else:
        print('No dockerfile and config is found. Change your directory where dockerfile is located.')

def registryLogin():
    #userRegistry = str(input('1. Docker 2. Other'))
    userPwdSelection = str(input("Do you want to load password from file or directly write your password? 1. Direct input 2. File"))
    userName = str(input("Username: "))
        
    if userPwdSelection =="1":
        userPassword = str(input("Password: "))
        loginCommand = 'docker login --username ' + str(userName) + ' --password ' + userPassword
        os.system(loginCommand)
    
    if userPwdSelection =="2":
        userPwdFileDir = str(input("Provide the direction of the password"))
        loginCommand = 'cat ' + userPwdFileDir + ' | ' + 'docker login --username ' + userName + ' --password-stdin'
        print(loginCommand)
        os.system(loginCommand)
        return True
        
def dockerBuildSingleService():
    dockerConfig = checkDockerInfo()
    if dockerConfig == True:
        print('Docker will start Buidling')
    
    containerName = str(input('Provide container name.'))
    containerTag = str(input('Provide you tag. Default is latest. Press enter for default.'))
    containerNameTag = ""

    if containerTag == "":
        containerNameTag =containerName + ":latest"
    else:
        containerNameTag =containerName + ":"+ containerTag
    
    containerCreationCommand = "docker built -t " + containerNameTag + " ."
    print(containerCreationCommand)
    #os.system(containerCreationCommand)
    return containerNameTag

def dockerPushSingleService(singleServiceContainer):
    registrySelection = input(str("Select your registry. Default is Docker. Press enter for defualt"))
    if registrySelection == "" :
        print("Docker registry is selected.")
        print("Login will be attempted")
        loginSuccess=registryLogin()    
        print("Login to Docker registry is successful. Now image will be tagged and pushed.")
        registryTag = str(input("Give registry tag for pushing. default is", singleServiceContainer + "Press enter for default"))
        if registryTag == "":
            registryTag =singleServiceContainer
        containerRegistryTag = "docker tag " + singleServiceContainer + " " + registryTag
        print(containerRegistryTag)
        #os.system(containerRegistryTag)
        print("Image is tagged with ", registryTag, "Image will be pushed now")
        containerPushCommand = "docker push " + registryTag
        #os.system(containerPushCommand)
        print(containerPushCommand)
        print("Image has been pushed successfully")

def imagesList():
    currentImageListCommand = "docker ps"
    allImagelistCommand = "docker ps -a"
    userInput = str(input("1. current images list 2. All images list"))
    if userInput =="1":
        os.system(currentImageListCommand)
    if userInput =="2":
        os.system(allImagelistCommand)

def main():
    if userPushSelection =="1":
        singleServiceContainer = dockerBuildSingleService()
        print(singleServiceContainer, "image has been created but not pushed. ")
     
    if userPushSelection == "2":
        singleServiceContainer = dockerBuildSingleService()
        print("Pushing is starting ", singleServiceContainer)
        dockerPushSingleService(singleServiceContainer)

  if userPushSelection == "3":
      imagesList()       

main()

