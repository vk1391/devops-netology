1.	```"HTTP/1.1 301 Moved Permanently
	cache-control: no-cache, no-store, must-revalidate
	location: https://stackoverflow.com/questions
	x-request-guid: 03c7d306-3889-4227-8855-fd4abf9f7916
	feature-policy: microphone 'none'; speaker 'none'
	content-security-policy: upgrade-insecure-requests; frame-ancestors 'self' 	https://stackexchange.com
	Accept-Ranges: bytes
	Date: Mon, 11 Oct 2021 13:05:12 GMT
	Via: 1.1 varnish
	Connection: close
	X-Served-By: cache-ams21053-AMS
	X-Cache: MISS
	X-Cache-Hits: 0
	X-Timer: S1633957513.687644,VS0,VE74
	Vary: Fastly-SSL
	X-DNS-Prefetch-Control: off
	Set-Cookie: prov=91915ec2-3bd6-e3a9-5077-9819628df133; domain=.stackoverflow.com; 	expires=Fri, 01-Jan-2055 00:00:00 GMT; path=/; HttpOnly"```
	Происходит перевод на https

3-4.``` 
	route:          217.197.224.0/20
	descr:          SEVEREN
	origin:         AS24739
	mnt-by:         SEVEREN-MNT
	created:        2009-02-27T07:51:44Z
	last-modified:  2009-02-27T07:51:44Z
	source:         RIPE 
```

5-6. ```	traceroute -An 8.8.8.8
	traceroute to 8.8.8.8 (8.8.8.8), 30 hops max, 60 byte packets
 	1  10.0.2.2 [*]  0.246 ms  0.199 ms  0.172 ms
 	2  10.0.2.2 [*]  4.622 ms  7.765 ms  7.659 ms
	не видит за натом
	mtr видит  mtr -y 0 8.8.8.8
	 1. AS???    _gateway                                                         0.0%    17    	0.5   0.5   0.2   0.8   0.1
	 2. AS???    172.20.0.1                                                       0.0%    17    4.6   4.6   2.3   8.1   1.2
 	3. AS24739  217.197.228.105                                                  0.0%    17    5.3   6.7   3.4  10.4   1.9
	 4. AS24739  93.174.247.254                                                   0.0%    17    9.0   5.6   3.6   9.0   1.3
	 5. AS24739  93.174.247.253                                                   0.0%    16    5.7   6.2   3.5  10.8   1.7
	 6. AS24739  93.174.240.20                                                    0.0%    16    6.2   6.4   4.2   9.4   1.4
	 7. AS24739  93.174.244.94                                                    0.0%    16    6.2   5.5   4.8   6.2   0.4
	 8. AS15169  74.125.244.133                                                   0.0%    16    6.2   5.5   3.4   7.2   0.9
	 9. AS15169  142.251.61.221                                                   0.0%    16   11.9  10.6   7.7  14.1   1.6
	10. AS15169  216.239.57.5                                                     0.0%    16    9.3   9.0   7.0  11.0   1.0
	11. (waiting for reply)
	12. (waiting for reply)
	13. (waiting for reply)
	14. (waiting for reply)
	15. (waiting for reply)
	16. (waiting for reply)
	17. (waiting for reply)
	18. (waiting for reply)
	19. (waiting for reply)
	20. AS15169  dns.google                                                       0.0%    16    8.4   9.4   7.0  12.1   1.6	
```
7. ```	 ANSWER SECTION:
	dns.google.             719     IN      A       8.8.4.4
	dns.google.             719     IN      A       8.8.8.8
```
8.```	root@vagrant:~# dig -x 8.8.8.8

 	DiG 9.16.1-Ubuntu <<>> -x 8.8.8.8
	global options: +cmd
	Got answer:
	->>HEADER<<- opcode: QUERY, status: NOERROR, id: 1737
	flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

	OPT PSEUDOSECTION:
	EDNS: version: 0, flags:; udp: 65494
	QUESTION SECTION:
	8.8.8.8.in-addr.arpa.          IN      PTR

	ANSWER SECTION:
	8.8.8.8.in-addr.arpa.   6660    IN      PTR     dns.google. ```

