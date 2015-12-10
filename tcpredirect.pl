#!/usr/bin/env perl

use warnings;
no warnings 'experimental';
use strict;
use feature "switch";
$\ = $/;

unless (@ARGV){
print <<HELP;
tcpredirect.pl [LISTEN PORT] [DESTINATION ADRESS] [DESTINATION PORT]
This program redirects all traffic from LISTEN PORT to DESTINATION ADRESS:DESTINATION PORT
HELP
exit;
}

my ($cmd, $local_port, $remote_ip, $remote_port) = @ARGV;

given($cmd){
    system("iptables -L -vt nat") when /list/i;
    system("iptables -F -vt nat") when /clean/i;
    when(/forward/i){
        system("echo 1 > /proc/sys/net/ipv4/ip_forward");
        system("iptables -t nat -A PREROUTING -p tcp --dport $local_port -j DNAT --to-destination $remote_ip:$remote_port");
        system("iptables -t nat -A POSTROUTING -j MASQUERADE");
        print "Succsessfully redirected $local_port to $remote_ip:$remote_port";
    }
}
