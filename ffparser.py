import subprocess

def fasff():
    
    ffresult = subprocess.run(["fastfetch" , "-l", "none"] , capture_output=True,text=True,)

    return ffresult.stdout[:942]
