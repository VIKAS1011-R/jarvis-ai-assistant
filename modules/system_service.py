#!/usr/bin/env python3
"""
System Information Service
Provides system information and basic file management
"""

import psutil
import os
import platform
import shutil
from datetime import datetime
from typing import Optional, List, Dict

class SystemService:
    def __init__(self):
        """Initialize system service"""
        pass
    
    def get_system_info(self) -> str:
        """Get general system information"""
        try:
            # Basic system info
            system = platform.system()
            release = platform.release()
            version = platform.version()
            machine = platform.machine()
            processor = platform.processor()
            
            # CPU info
            cpu_count = psutil.cpu_count()
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory info
            memory = psutil.virtual_memory()
            memory_total_gb = round(memory.total / (1024**3), 1)
            memory_used_gb = round(memory.used / (1024**3), 1)
            memory_percent = memory.percent
            
            info = f"System: {system} {release}, "
            info += f"CPU: {cpu_count} cores at {cpu_percent}% usage, "
            info += f"Memory: {memory_used_gb} GB of {memory_total_gb} GB used ({memory_percent}%)"
            
            return info
            
        except Exception as e:
            print(f"System info error: {e}")
            return "Unable to retrieve system information."
    
    def get_disk_space(self, path: str = "C:\\") -> str:
        """Get disk space information"""
        try:
            if platform.system() != "Windows":
                path = "/"
            
            disk_usage = shutil.disk_usage(path)
            
            total_gb = round(disk_usage.total / (1024**3), 1)
            used_gb = round((disk_usage.total - disk_usage.free) / (1024**3), 1)
            free_gb = round(disk_usage.free / (1024**3), 1)
            used_percent = round((used_gb / total_gb) * 100, 1)
            
            return f"Disk space on {path}: {used_gb} GB used, {free_gb} GB free, {total_gb} GB total ({used_percent}% used)"
            
        except Exception as e:
            print(f"Disk space error: {e}")
            return "Unable to retrieve disk space information."
    
    def get_battery_info(self) -> str:
        """Get battery information (for laptops)"""
        try:
            battery = psutil.sensors_battery()
            
            if battery is None:
                return "No battery detected. This appears to be a desktop computer."
            
            percent = round(battery.percent, 1)
            plugged = "plugged in" if battery.power_plugged else "not plugged in"
            
            if battery.secsleft != psutil.POWER_TIME_UNLIMITED and battery.secsleft != psutil.POWER_TIME_UNKNOWN:
                hours = battery.secsleft // 3600
                minutes = (battery.secsleft % 3600) // 60
                time_left = f", approximately {hours} hours and {minutes} minutes remaining"
            else:
                time_left = ""
            
            return f"Battery: {percent}% charged, {plugged}{time_left}"
            
        except Exception as e:
            print(f"Battery info error: {e}")
            return "Unable to retrieve battery information."
    
    def get_network_info(self) -> str:
        """Get network information"""
        try:
            # Get network interfaces
            interfaces = psutil.net_if_addrs()
            active_interfaces = []
            
            for interface_name, interface_addresses in interfaces.items():
                for address in interface_addresses:
                    if address.family == 2:  # IPv4
                        if not address.address.startswith('127.'):  # Skip localhost
                            active_interfaces.append(f"{interface_name}: {address.address}")
            
            if active_interfaces:
                return f"Network interfaces: {', '.join(active_interfaces)}"
            else:
                return "No active network interfaces found."
                
        except Exception as e:
            print(f"Network info error: {e}")
            return "Unable to retrieve network information."
    
    def get_running_processes(self, limit: int = 5) -> str:
        """Get top running processes by CPU usage"""
        try:
            processes = []
            
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    proc_info = proc.info
                    if proc_info['cpu_percent'] > 0:
                        processes.append(proc_info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # Sort by CPU usage
            processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
            
            if not processes:
                return "No processes with significant CPU usage found."
            
            result = f"Top {min(limit, len(processes))} processes by CPU usage: "
            
            for i, proc in enumerate(processes[:limit]):
                name = proc['name']
                cpu = round(proc['cpu_percent'], 1)
                memory = round(proc['memory_percent'], 1)
                result += f"{name} ({cpu}% CPU, {memory}% memory)"
                if i < min(limit, len(processes)) - 1:
                    result += ", "
            
            return result
            
        except Exception as e:
            print(f"Process info error: {e}")
            return "Unable to retrieve process information."
    
    def create_folder(self, folder_name: str, location: str = None) -> str:
        """Create a new folder"""
        try:
            if location is None:
                location = os.path.expanduser("~/Desktop")
            
            folder_path = os.path.join(location, folder_name)
            
            if os.path.exists(folder_path):
                return f"Folder '{folder_name}' already exists at {location}"
            
            os.makedirs(folder_path)
            return f"Created folder '{folder_name}' at {location}"
            
        except Exception as e:
            print(f"Create folder error: {e}")
            return f"Unable to create folder '{folder_name}'"
    
    def list_files(self, directory: str = None, limit: int = 10) -> str:
        """List files in a directory"""
        try:
            if directory is None:
                directory = os.path.expanduser("~/Desktop")
            
            if not os.path.exists(directory):
                return f"Directory '{directory}' does not exist."
            
            files = []
            folders = []
            
            for item in os.listdir(directory):
                item_path = os.path.join(directory, item)
                if os.path.isfile(item_path):
                    files.append(item)
                elif os.path.isdir(item_path):
                    folders.append(item)
            
            result = f"Contents of {directory}: "
            
            if folders:
                result += f"{len(folders)} folders"
                if len(folders) <= 5:
                    result += f" ({', '.join(folders[:5])})"
                result += ", "
            
            if files:
                result += f"{len(files)} files"
                if len(files) <= 5:
                    result += f" ({', '.join(files[:5])})"
            
            if not folders and not files:
                result += "empty"
            
            return result
            
        except Exception as e:
            print(f"List files error: {e}")
            return f"Unable to list files in '{directory}'"
    
    def get_uptime(self) -> str:
        """Get system uptime"""
        try:
            boot_time = psutil.boot_time()
            uptime_seconds = datetime.now().timestamp() - boot_time
            
            days = int(uptime_seconds // 86400)
            hours = int((uptime_seconds % 86400) // 3600)
            minutes = int((uptime_seconds % 3600) // 60)
            
            uptime_parts = []
            if days > 0:
                uptime_parts.append(f"{days} day{'s' if days != 1 else ''}")
            if hours > 0:
                uptime_parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
            if minutes > 0:
                uptime_parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
            
            if not uptime_parts:
                return "System uptime: less than a minute"
            
            return f"System uptime: {', '.join(uptime_parts)}"
            
        except Exception as e:
            print(f"Uptime error: {e}")
            return "Unable to retrieve system uptime."

# Test function
def test_system_service():
    """Test the system service"""
    print("Testing System Service")
    print("=" * 30)
    
    system = SystemService()
    
    print("1. System info:")
    print(f"   {system.get_system_info()}")
    
    print("\n2. Disk space:")
    print(f"   {system.get_disk_space()}")
    
    print("\n3. Battery info:")
    print(f"   {system.get_battery_info()}")
    
    print("\n4. Network info:")
    print(f"   {system.get_network_info()}")
    
    print("\n5. Running processes:")
    print(f"   {system.get_running_processes(3)}")
    
    print("\n6. System uptime:")
    print(f"   {system.get_uptime()}")

if __name__ == "__main__":
    test_system_service()