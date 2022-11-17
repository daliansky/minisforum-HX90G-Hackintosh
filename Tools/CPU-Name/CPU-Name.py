import subprocess
import platform
from Scripts import plist, utils

class CPUName:
    def __init__(self, **kwargs):
        self.u = utils.Utils("CPU-Name")
        self.plist_path = None
        self.plist_data = {}
        self.clear_empty = True
        self.detected = self.detect_cores()
        self.cpu_model = self.detect_cpu_model()

    def ensure_path(self, plist_data, path_list, final_type = list):
        if not path_list: return plist_data
        last = plist_data
        for index,path in enumerate(path_list):
            if not path in last:
                if index >= len(path_list)-1:
                    last[path] = final_type()
                else:
                    last[path] = {}
            last = last[path]
        return plist_data

    def select_plist(self):
        while True:
            self.u.head("Select Plist")
            print("")
            print("M. Return To Menu")
            print("Q. Quit")
            print("")
            plist_path = self.u.grab("Please drag and drop your config.plist here:  ")
            if not len(plist_path): continue
            elif plist_path.lower() == "m": return
            elif plist_path.lower() == "q": self.u.custom_quit()
            path_checked = self.u.check_path(plist_path)
            if not path_checked: continue
            # Got a valid path here - let's try to load it
            try:
                with open(path_checked,"rb") as f:
                    plist_data = plist.load(f)
                if not isinstance(plist_data,dict):
                    raise Exception("Plist root is not a dictionary")
            except Exception as e:
                self.u.head("Error Loading Plist")
                print("\nCould not load {}:\n\n{}\n\n".format(path_checked,repr(e)))
                self.u.grab("Press [enter] to return...")
                continue
            # Got valid plist data - let's store the vars and return
            self.plist_path = path_checked
            self.plist_data = plist_data
            return (path_checked,plist_data)

    def get_value(self, plist_data, search="revcpuname"):
        boot_args = plist_data.get("NVRAM",{}).get("Add",{}).get("7C436110-AB2A-4BBB-A880-FE41995C9F82",{}).get("boot-args","")
        nvram_val = plist_data.get("NVRAM",{}).get("Add",{}).get("4D1FDA02-38C7-4A6A-9CC6-4BCCA8B30102",{}).get(search,"")
        boota_val = ""
        for arg in boot_args.split():
            if not arg.startswith(search+"="): continue
            boota_val = arg.split("=")[-1]
            break # Only take the first instance
        return (boota_val,nvram_val)

    def get_cpu_name(self, plist_data):
        return self.get_value(plist_data,"revcpuname")

    def get_rev_cpu(self, plist_data):
        return self.get_value(plist_data,"revcpu")

    def get_proc_type(self, plist_data):
        return plist_data.get("PlatformInfo",{}).get("Generic",{}).get("ProcessorType",0)

    def get_kext(self, plist_data):
        kext_list = plist_data.get("Kernel",{}).get("Add",[])
        found = enabled = False
        for kext in kext_list:
            if kext.get("ExecutablePath","").lower() == "contents/macos/restrictevents":
                found = True
                if kext.get("Enabled"):
                    enabled = True
                    break
        return (found,enabled)

    def get_new_proc_type(self, plist_data):
        while True:
            p_type  = self.get_proc_type(plist_data)
            p_label = " (8+ Core)" if p_type == 3841 else " (1, 2, 4, or 6 Core)" if p_type == 1537 else " (Must be 0x0601 or 0x0F01 to work)"
            self.u.head("ProcessorType")
            print("")
            print("Current Processor Type: {}{}".format(self.get_hex(p_type),p_label))
            print("")
            print("1. Set to 0x0601 for 1, 2, 4, or 6 Core")
            print("2. Set to 0x0F01 for 8+ Core")
            print("3. Reset to the default 0x00")
            print("")
            if self.detected != -1:
                print("L. Use Local Machine's Value ({:,} Core{} = {})".format(self.detected, "" if self.detected==1 else "s", "0x0601" if self.detected < 8 else "0x0F01"))
            print("M. Return To Menu")
            print("Q. Quit")
            print("")
            proc = self.u.grab("Please select an option:  ")
            if not len(proc): continue
            if proc.lower() == "m": return None
            elif proc.lower() == "q": self.u.custom_quit()
            elif proc == "1": return 1537
            elif proc == "2": return 3841
            elif proc == "3": return 0
            elif self.detected != -1 and proc.lower() == "l": return 1537 if self.detected < 8 else 3841

    def detect_cpu_model(self):
        try:
            _platform = platform.system().lower()
            if _platform == "darwin":
                return subprocess.check_output(["sysctl", "-n", "machdep.cpu.brand_string"]).decode().strip()
            elif _platform == "windows":
                return subprocess.check_output(["wmic", "cpu", "get", "Name"]).decode().split("\n")[1].strip()
            elif _platform == "linux":
                data = subprocess.check_output(["cat", "/proc/cpuinfo"]).decode().split("\n")
                for line in data:
                    if line.startswith("model name"):
                        return ": ".join([x for x in line.split(": ")[1:]])
        except:
            pass
        return ""

    def detect_cores(self):
        try:
            _platform = platform.system().lower()
            if _platform == "darwin":
                return int(subprocess.check_output(["sysctl", "-a", "machdep.cpu.core_count"]).decode().split(":")[1].strip())
            elif _platform == "windows":
                return int(subprocess.check_output(["wmic", "cpu", "get", "NumberOfCores"]).decode().split("\n")[1].strip())
            elif _platform == "linux":
                data = subprocess.check_output(["cat", "/proc/cpuinfo"]).decode().split("\n")
                for line in data:
                    if line.startswith("cpu cores"):
                        return int(line.split(":")[1].strip())
        except:
            pass
        return -1

    def set_values(self, revcpu, cpuname, proctype, plist_data):
        # Clear any prior values and ensure pathing
        plist_data = self.clear_values(plist_data)
        plist_data = self.ensure_path(plist_data,["NVRAM","Add","4D1FDA02-38C7-4A6A-9CC6-4BCCA8B30102"],dict)
        plist_data = self.ensure_path(plist_data,["PlatformInfo","Generic","ProcessorType"],int)
        # Set our new values
        plist_data["NVRAM"]["Add"]["4D1FDA02-38C7-4A6A-9CC6-4BCCA8B30102"]["revcpu"] = revcpu
        plist_data["NVRAM"]["Add"]["4D1FDA02-38C7-4A6A-9CC6-4BCCA8B30102"]["revcpuname"] = cpuname
        plist_data["PlatformInfo"]["Generic"]["ProcessorType"] = proctype
        return plist_data

    def clear_values(self, plist_data):
        # Ensure Delete values exist so we can prevent old values from sticking
        plist_data = self.ensure_path(plist_data,["NVRAM","Delete","4D1FDA02-38C7-4A6A-9CC6-4BCCA8B30102"],list)
        plist_data = self.ensure_path(plist_data,["NVRAM","Delete","7C436110-AB2A-4BBB-A880-FE41995C9F82"],list)
        # Gather our values
        boot_args = plist_data["NVRAM"].get("Add",{}).get("7C436110-AB2A-4BBB-A880-FE41995C9F82",{}).get("boot-args","")
        nv_a_val  = plist_data["NVRAM"].get("Add",{}).get("4D1FDA02-38C7-4A6A-9CC6-4BCCA8B30102",{})
        nv_d_val  = plist_data["NVRAM"]["Delete"]["4D1FDA02-38C7-4A6A-9CC6-4BCCA8B30102"]
        # Walk boot args to see if we use any revcpu* values and remove them
        if any(x in boot_args for x in ("revcpu=","revcpuname=")):
            boot_args = " ".join([x for x in boot_args.split() if not x.startswith(("revcpu=","revcpuname="))])
            plist_data["NVRAM"]["Add"]["7C436110-AB2A-4BBB-A880-FE41995C9F82"]["boot-args"] = boot_args
        # Remove them from the NVRAM -> Add section
        if any(x in nv_a_val for x in ("revcpu","revcpuname")):
            for x in ("revcpu","revcpuname"):
                nv_a_val.pop(x,None)
            if nv_a_val:
                plist_data["NVRAM"]["Add"]["4D1FDA02-38C7-4A6A-9CC6-4BCCA8B30102"] = nv_a_val
            elif self.clear_empty:
                # Clean out the UUID if empty
                plist_data["NVRAM"]["Add"].pop("4D1FDA02-38C7-4A6A-9CC6-4BCCA8B30102",None)
        # Ensure they remain in the NVRAM -> Delete section to prevent stuck values
        for x in ("revcpu","revcpuname"):
            if x in nv_d_val: continue
            nv_d_val.append(x)
        # Make sure we override boot-args to avoid any stickage too
        if not "boot-args" in plist_data["NVRAM"]["Delete"]["7C436110-AB2A-4BBB-A880-FE41995C9F82"]:
            plist_data["NVRAM"]["Delete"]["7C436110-AB2A-4BBB-A880-FE41995C9F82"].append("boot-args")
        plist_data["NVRAM"]["Delete"]["4D1FDA02-38C7-4A6A-9CC6-4BCCA8B30102"] = nv_d_val
        if plist_data.get("PlatformInfo",{}).get("Generic",{}).get("ProcessorType",0) != 0:
            plist_data["PlatformInfo"]["Generic"]["ProcessorType"] = 0
        return plist_data

    def get_hex(self, value, pad_to=2):
        if not isinstance(value,int): return ""
        h = hex(value)[2:]
        return "0x"+("0"*(len(h)%pad_to))+h.upper()

    def get_new_cpu_name(self, plist_data):
        while True:
            cpu_nam = self.get_cpu_name(plist_data)
            self.u.head("New CPU Name")
            print("")
            print("Current CPU Name: {}".format(cpu_nam[0]+" (boot-arg)" if cpu_nam[0] else cpu_nam[1] if cpu_nam[1] else "Not Set"))
            print("")
            if self.cpu_model:
                print("L. Use Local Machine's Value ({})".format(self.cpu_model))
            print("M. Return To Menu")
            print("Q. Quit")
            print("")
            name = self.u.grab("Please enter a new CPU name:  ")
            if not len(name): continue
            elif name.lower() == "m": return
            elif name.lower() == "q": self.u.custom_quit()
            elif self.cpu_model and name.lower() == "l": return self.cpu_model
            return name

    def save_plist(self):
        try:
            with open(self.plist_path,"wb") as f:
                plist.dump(self.plist_data,f)
        except Exception as e:
            self.u.head("Error Saving Plist")
            print("\nCould not save {}:\n\n{}\n\n".format(self.plist_path,repr(e)))
            self.u.grab("Press [enter] to return...")
            return False
        return True
    
    def main(self):
        while True:
            cpu_rev = self.get_rev_cpu(self.plist_data)
            cpu_nam = self.get_cpu_name(self.plist_data)
            p_type  = self.get_proc_type(self.plist_data)
            p_label = " (8+ Core)" if p_type == 3841 else " (1, 2, 4, or 6 Core)" if p_type == 1537 else " (Must be 0x0601 or 0x0F01 to work!)"
            f,e     = self.get_kext(self.plist_data)
            k_label = "Not Found (Must be present and Enabled to work!)" if not f else "Disabled (Must be Enabled to work!)" if not e else "Found and Enabled"
            self.u.head()
            print("")
            print("Selected Plist: {}".format(self.plist_path))
            print("Rev CPU Name:   {}".format("" if not self.plist_path else cpu_nam[0]+" (boot-arg)" if cpu_nam[0] else cpu_nam[1] if cpu_nam[1] else "Not Set"))
            print("Rev CPU:        {}".format("" if not self.plist_path else cpu_rev[0]+" (boot-arg)" if cpu_rev[0] else cpu_rev[1] if cpu_rev[1] else "Not Set"))
            print("Processor Type: {}{}".format("" if not self.plist_path else self.get_hex(p_type),"" if not self.plist_path else p_label))
            print("RestrictEvents: {}".format("" if not self.plist_path else k_label))
            print("")
            print("Note:  Changes are saved to the target plist immediately.")
            print("       Make sure you keep a backup!")
            print("")
            print("1. Change CPU Name")
            print("2. Change Processor Type")
            print("3. Clear CPU Name, Rev CPU, and Processor Type")
            print("4. Select Plist")
            print("")
            print("Q. Quit")
            print("")
            menu = self.u.grab("Please select an option:  ")
            if not len(menu): continue
            elif menu.lower() == "q": self.u.custom_quit()
            if menu in ("1","2","3") and not self.plist_path:
                self.select_plist()
                if not self.plist_path: continue
                p_type = self.get_proc_type(self.plist_data) # Gather new proc type after loading
            if menu == "1":
                if not p_type in (3841,1537):
                    new_type = self.get_new_proc_type(self.plist_data)
                    if new_type is None: continue
                    p_type = new_type
                new_name = self.get_new_cpu_name(self.plist_data)
                if new_name is None: continue
                self.plist_data = self.set_values(1,new_name,p_type,self.plist_data)
                self.save_plist()
            elif menu == "2":
                new_type = self.get_new_proc_type(self.plist_data)
                if new_type is None: continue
                self.plist_data = self.ensure_path(self.plist_data,["PlatformInfo","Generic","ProcessorType"],int)
                self.plist_data["PlatformInfo"]["Generic"]["ProcessorType"] = new_type
                self.save_plist()
            elif menu == "3":
                self.plist_data = self.clear_values(self.plist_data)
                self.save_plist()
            elif menu == "4":
                self.select_plist()

c = CPUName()
c.main()
