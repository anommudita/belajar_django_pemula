
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

# message flash django
from django.contrib import messages

# import data models
from .models import Device

# import paramiko dam time
import paramiko, time

# Create your views here.
def devices(request):

    # menampilkan semua data yang ada di database
    all_devices = Device.objects.all()

    # cisco devices dengan filter
    cisco_device = Device.objects.filter(vendor='cisco')

    # mikrotik devices dengan filter
    mikrotik_device = Device.objects.filter(vendor='mikrotik')


    # get all data from database table device
    devices = Device.objects.all()
    
    people = [
        {'id' : 1, 'name' : "Gus Anom"},
        {'id' : 2, 'name' : "Surya Dharma"},
        {'id' : 3, 'name' : "Dek Angga"},
    ]

    context = {
        'title' : "Devices",
        'active_devices' : 'active',
        'people' : people,
        'devices' : devices,
        'all_devices' : len(all_devices),
        'cisco_device' : len(cisco_device),
        'mikrotik_device' : len(mikrotik_device),
    }

    return render(request, 'devices.html', context)

def tambah_device(request):

    if request.method == "POST":
        hostname = request.POST.get('hostname')
        ip_address = request.POST.get('ip_address')
        username = request.POST.get('username')
        password = request.POST.get('password_device')
        vendor = request.POST.get('vendor')


        if hostname == "" or ip_address == "" or username == "" or password == "" or vendor == "":
            messages.error(request, "All fields must be filled")
            return redirect('devices')

        # insert data to database
        add_device = Device(hostname=hostname, ip_address=ip_address, username=username, password=password, vendor=vendor)
        add_device.save()

        return redirect('devices')
    else:
        messages.error(request, "Failed to add device")
        
    context = {
        'title' : "Insert Devices",
        'active_devices' : 'active',
    }
    return render(request, 'crud_devices/tambah_devices.html', context)


def edit_device(request, id_device):

    # data by id
    device = Device.objects.get(id=id_device)
    
    if request.method == "POST":
        hostname = request.POST.get('edit_hostname')
        ip_address = request.POST.get('edit_ip_address')
        username = request.POST.get('edit_username')
        password = request.POST.get('edit_password_device')
        vendor = request.POST.get('edit_vendor')

        # Update data in the database
        device.hostname = hostname
        device.ip_address = ip_address
        device.username = username
        device.password = password
        device.vendor = vendor
        device.save()

        return redirect('devices')
    else:
        pass
        
    context = {
        'title' : "Edit Devices",
        'active_devices' : 'active',
        'device' : device
    }

    return render(request, 'crud_devices/edit_devices.html', context)


def delete_device(request, id_device):
    # data by id
    device = Device.objects.get(id=id_device)

    # delete data in the database
    device.delete()
    return redirect('devices')


def configure(request):
    
    # jika menekan tombol submit
    if request.method == 'POST':

        selected_devices_id = request.POST.getlist('device')
        mikrotik_command = request.POST['mikrotik_command'].splitlines()
        cisco_command = request.POST['cisco_command'].splitlines()

        for x in selected_devices_id:

            # # log
            try:
                dev = get_object_or_404(Device, pk=x)
                ssh_clinet = paramiko.SSHClient()
                ssh_clinet.set_missing_host_key_policy(
                    paramiko.AutoAddPolicy())
                ssh_clinet.connect(hostname=dev.ip_address, username=dev.username, password=dev.password)

                if dev.vendor.lower() == 'cisco':
                    conn = ssh_clinet.invoke_shell()
                    conn.send('conf t\n')
                    for cmd in cisco_command:
                        conn.send(cmd + '\n')
                        time.sleep(1)
                else:
                    for cmd in mikrotik_command:
                        ssh_clinet.exec_command(cmd)

                # success configure
                return redirect('devices')

            except Exception as e:
                print(e)
                # failed configure
                return redirect('devices')

    else:
        devices = Device.objects.all()

        context = {
        'title' : "Configure Devices",
        'active_config' : 'active',
        'devices' : devices
        }

        return render(request, 'config.html', context)


