import subprocess
import sys
import importlib.util

def check_conan_installed():
    """检查Conan是否已安装"""
    try:
        # 尝试导入conan模块
        spec = importlib.util.find_spec("conans")
        if spec is not None:
            print("Conan已安装")
            # 检查Conan版本
            result = subprocess.run(["conan", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                print(result.stdout.strip())
                return True
        return False
    except Exception as e:
        print(f"检查Conan安装时出错: {e}")
        return False

def install_conan():
    """安装Conan包管理器"""
    print("开始安装Conan...")
    try:
        # 使用pip安装Conan
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "conan"],
            capture_output=True,
            text=True,
            check=True
        )
        print("Conan安装成功")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Conan安装失败: {e.stderr}")
        return False
    except Exception as e:
        print(f"发生未知错误: {e}")
        return False

def verify_conan_installation():
    """验证Conan安装并显示版本信息"""
    try:
        result = subprocess.run(["conan", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("Conan安装验证成功:")
            print(result.stdout.strip())
            return True
        else:
            print(f"Conan验证失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"验证过程中出错: {e}")
        return False

def main():
    """主函数，协调Conan的检查、安装和验证"""
    if not check_conan_installed():
        if install_conan():
            verify_conan_installation()
        else:
            print("Conan安装过程中出现问题，请手动安装。")
            print("可以使用命令: pip install conan")
    else:
        print("Conan已安装且可正常使用。")

if __name__ == "__main__":
    main()