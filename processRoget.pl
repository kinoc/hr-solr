$src='E:\DIGITSVM\OpenCogShared\kinoc\hr-solr\roget15c.txt';
open(FIN,"<$src");
while($line =<FIN>)
{
	chomp($line);
	if ($line =~/(\#)/)
	{
	 $master = <FIN>;
	 chomp($master);
	 next;
	}
	if ($line =~ /^(\#|N|V|Adj|Adv|Phr|adj|adv|Int)/)
	{
	 next;
	}
	$line =~ s/[0-9]+/ /gi;
	$line =~ s/[^a-zA-Z0-9 \,]/\, /gi;
	$line =~ s/\, \,/\, /gi;
	$line =~ s/^I\,/ /;
	$line =~ s/^\,/ /;
	while ($line =~ /  /) {$line =~ s/  / /gi;}
	while ($line =~ /, /) {$line =~ s/, /,/gi;}
	my @p = split(/\,/,$line);
	# $count = scalar @p;
	# if ($count<2) {next;}
	
	$out="";
	foreach $x (@p)
	{
	while($x =~ /^ /) { $x =~ s/^ //;}
	while($x =~ / $/) { $x =~ s/ $//;}
	while($x =~ /The /) { $x =~ s/The //;}
	 
	 if ($x =~ / /) {next;}
	 
	 if (length($x)<3) {next;}
	 if (length($out)>1) {$out .=",";}
	 $out .= $x;
	}
	while ($out =~ /  /) {$out =~ s/  / /gi;}
	while ($out =~ /, /) {$out =~ s/, /,/gi;}
	if ((length($out)>1)&&($out =~ /\,/))
	{
	print "$out\n";
	}
}
close(FIN);