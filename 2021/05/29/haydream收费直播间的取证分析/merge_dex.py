if __name__ == "__main__":
    if len(sys.argv) < 3 :
        print("start error")
        sys.exit()

    print(sys.argv[1], sys.argv[2])
    
path = sys.argv[1] #文件夹目录
files= os.listdir(path) #得到文件夹下的所有文件名称
s = []
for file in files: #遍历文件夹
    if file.find("dex") > 0: ## 查找dex 文件
        sh = 'jadx -j 1 -r -d ' + sys.argv[2] + " " + path + file
        print(sh)
        os.system(sh)