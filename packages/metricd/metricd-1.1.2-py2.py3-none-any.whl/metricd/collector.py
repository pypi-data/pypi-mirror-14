import os
import socket

import psutil


class Collector(object):
    old_values = {}
    interval = None
    hostname = None

    def __init__(self, interval, hostname):
        self.interval = interval
        self.hostname = hostname

    def collect(self):
        NotImplemented()

    def merge_dicts(self, *dict_args):
        result = {}
        for dictionary in dict_args:
            result.update(dictionary)
        return result

    def get_derived(self, key, value):
        if key in self.old_values:
            diff = value - self.old_values[key]
            self.old_values[key] = value
            return diff / self.interval
        else:
            self.old_values[key] = value
            return 0


class SystemCollector(Collector):
    def collect(self):
        return self.merge_dicts(
                self.collect_load(),
                self.collect_memory(),
                self.collect_swap(),
                self.collect_cpu(),
                self.collect_interfaces(),
                self.collect_io(),
                self.collect_disks(),
                self.collect_connections(),
                self.collect_metadata()
        )

    def collect_load(self):
        load_averages = os.getloadavg()

        return {
            'load.shortterm': load_averages[0],
            'load.midterm': load_averages[1],
            'load.longterm': load_averages[2]
        }

    def collect_memory(self):
        virtual_memory = psutil.virtual_memory()

        results = {
            'memory.percent': virtual_memory.percent,
            'memory.total': virtual_memory.total,
            'memory.used': virtual_memory.used,
            'memory.free': virtual_memory.free,
            'memory.available': virtual_memory.available
        }

        if hasattr(virtual_memory, "cached"):
            results['memory.cached'] = virtual_memory.cached
        if hasattr(virtual_memory, "buffered"):
            results['memory.buffered'] = virtual_memory.buffers

        return results

    def collect_swap(self):
        swap_memory = psutil.swap_memory()

        return {
            'swap.percent': swap_memory.percent,
            'swap.total': swap_memory.total,
            'swap.used': swap_memory.used,
            'swap.free': swap_memory.free
        }

    def collect_cpu(self):
        cpu = psutil.cpu_times_percent()

        results = {
            'cpu.cores': psutil.cpu_count(),
            'cpu.percent': (cpu.user + cpu.nice + cpu.system),
            'cpu.user': cpu.user,
            'cpu.nice': cpu.nice,
            'cpu.system': cpu.system,
            'cpu.idle': cpu.idle
        }

        if hasattr(cpu, "iowait"):
            results['cpu.iowait'] = cpu.iowait
        if hasattr(cpu, "irq"):
            results['cpu.irq'] = cpu.irq
        if hasattr(cpu, "softirq"):
            results['cpu.softirq'] = cpu.softirq
        if hasattr(cpu, "steal"):
            results['cpu.steal'] = cpu.steal
        if hasattr(cpu, "guest"):
            results['cpu.guest'] = cpu.guest
        if hasattr(cpu, "guestnice"):
            results['cpu.guestnice'] = cpu.guestnice

        return results

    def collect_interfaces(self):
        interfaces = psutil.net_io_counters(pernic=True)

        new_values = {}
        for interface in interfaces:
            new_values['network.%s.bytes.sent' % interface] = interfaces[interface].bytes_sent
            new_values['network.%s.bytes.received' % interface] = interfaces[interface].bytes_recv
            new_values['network.%s.packets.sent' % interface] = interfaces[interface].packets_sent
            new_values['network.%s.packets.received' % interface] = interfaces[interface].packets_recv
            new_values['network.%s.errors.in' % interface] = interfaces[interface].errin
            new_values['network.%s.errors.out' % interface] = interfaces[interface].errout
            new_values['network.%s.drops.in' % interface] = interfaces[interface].dropin
            new_values['network.%s.drops.out' % interface] = interfaces[interface].dropout

        results = {}
        for key, value in new_values.items():
            results[key] = self.get_derived(key, value)

        return results

    def collect_io(self):
        io = psutil.disk_io_counters(perdisk=True)
        new_values = {}

        for disk in io:
            new_values['io.%s.ops.read' % disk] = io[disk].read_count
            new_values['io.%s.ops.write' % disk] = io[disk].write_count
            new_values['io.%s.bytes.read' % disk] = io[disk].read_bytes
            new_values['io.%s.bytes.write' % disk] = io[disk].write_bytes
            if hasattr(io[disk], "read_merged_count"):
                new_values['io.%s.merged.read' % disk] = io[disk].read_merged_count
            if hasattr(io[disk], "write_merged_count"):
                new_values['io.%s.merged.write' % disk] = io[disk].write_merged_count

        # TODO: read / write times?

        results = {}
        for key, value in new_values.items():
            results[key] = self.get_derived(key, value)

        return results

    def collect_disks(self):
        psutil.disk_partitions()
        partitions = psutil.disk_partitions(all=False)

        results = {}
        for part in partitions:
            usage = psutil.disk_usage(part.mountpoint)
            _, _, disk = part.device.rpartition("/")
            results['disk.%s.percent' % disk] = usage.percent
            results['disk.%s.total' % disk] = usage.total
            results['disk.%s.used' % disk] = usage.used
            results['disk.%s.free' % disk] = usage.free

        return results

    def collect_connections(self):
        try:
            results = {
                'connections/tcp4': len(psutil.net_connections("tcp4")),
                'connections/tcp6': len(psutil.net_connections("tcp6")),
                'connections/udp4': len(psutil.net_connections("udp4")),
                'connections/udp6': len(psutil.net_connections("udp6")),
                'connections/unix': len(psutil.net_connections("unix"))
            }

            results['connections/total'] = (results['connections/unix'] + results['connections/udp6'] +
                                            results['connections/udp4'] + results['connections/tcp4'] +
                                            results['connections/tcp6'])
            return results
        except psutil.AccessDenied:  # BSD / OSX needs root access for that
            return {}

    def collect_metadata(self):
        return {
            'metadata.hostname': self.hostname,
            'metadata.fqdn': socket.getfqdn(),
            'metadata.ip_address': socket.gethostbyname(socket.gethostname())
        }
