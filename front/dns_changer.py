import subprocess
import wmi
import sys
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def get_active_adapter():
    """
    بررسی آداپتورهای شبکه و انتخاب آداپتور فعال از بین Ethernet و Wi-Fi.
    در صورت فعال بودن هر دو، اولویت با Ethernet است.
    """
    c = wmi.WMI()
    ethernet_active = None
    wifi_active = None
    for nic in c.Win32_NetworkAdapter():
        if nic.NetConnectionID and nic.NetConnectionStatus == 2:
            if nic.NetConnectionID.lower() == "ethernet":
                ethernet_active = nic.NetConnectionID
            elif nic.NetConnectionID.lower() in ("wi-fi", "wifi"):
                wifi_active = nic.NetConnectionID

    return ethernet_active if ethernet_active else wifi_active

def change_dns(adapter_name):
    try:
        # تنظیم DNS اولیه به صورت استاتیک
        subprocess.run(
            f'netsh interface ipv4 set dnsservers name="{adapter_name}" static 178.22.122.100 primary',
            check=True, shell=True, 
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        # افزودن DNS ثانویه
        subprocess.run(
            f'netsh interface ipv4 add dnsservers name="{adapter_name}" 185.51.200.2 index=2',
            check=True, shell=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        return True
    except Exception as e:
        return False

def silent_change_dns():
    """
    تغییر DNS بدون نمایش هیچ پیامی
    """
    if not is_admin():
        # اجرای مجدد اسکریپت با دسترسی Administrator
        ctypes.windll.shell32.ShellExecuteW(
            None, 
            "runas", 
            sys.executable, 
            f'"{__file__}" --silent', 
            None, 
            0  # SW_HIDE - پنجره مخفی
        )
        sys.exit(0)  # خروج از برنامه پس از درخواست دسترسی ادمین

    adapter = get_active_adapter()
    if not adapter:
        return False

    return change_dns(adapter)

if __name__ == "__main__":
    if "--silent" in sys.argv:
        silent_change_dns()
    else:
        # برای سازگاری با نسخه قبلی
        import tkinter as tk
        from tkinter import messagebox
        
        root = tk.Tk()
        root.withdraw()

        adapter = get_active_adapter()
        if not adapter:
            messagebox.showerror("خطا", "هیچ آداپتور شبکه فعالی یافت نشد!")
            sys.exit(1)

        if change_dns(adapter):
            messagebox.showinfo("موفق", f"تنظیمات DNS برای آداپتور {adapter} با موفقیت تغییر یافت!")
        else:
            messagebox.showerror("خطا", "خطا در تغییر DNS")
