#��������������������������������������������������������������������
#�� pickup.pl for YY-BOARD
#�� Copyright isso. May, 2007
#�� http://swanbay-web.hp.infoseek.co.jp/index.html
#��������������������������������������������������������������������

#-------------------------------------------------
#  �֘A�X���b�h�\��
#-------------------------------------------------
sub pickup {
	local(%no,%re,%date,%name,%eml,%sub,%com,%url,%hos,%pw,%col,%tm,%sml,%author);
	local($i,$j,$hitnum);

	if ($in{'action'} eq "past") { $logfile = sprintf("%s/%04d.cgi", $pastdir,$in{'log'}); }

	# �L���e�ԍ�����
	$hitnum = 0;
	open(IN,"$logfile") || &error("���O�t�@�C�� $logfile ������܂���B");
	if ($in{'action'} ne "past") { $top = <IN>; }
	while (<IN>) {
		chomp;
		($no,$re) = split(/<>/);
		if ($in{'num'} eq $no) {
			if (!$re) { $hitnum = $no; } else { $hitnum = $re; }
		}
	}
	close(IN);

	if (!$hitnum) { &error("�Y�����郁�b�Z�[�W������܂���B"); }

	print "<div align=\"center\">\n";
	if ($in{'action'} eq "past") { $logname ="�ߋ����O"; } else { $logname ="�R�����g"; }
	print "[ �w��$logname (No\.$in{'num'}) �̊֘A�X���b�h��\\�����Ă��܂��B ]\n";

	# �L���X���b�h����
	$i = 0;
	open(IN,"$logfile") || &error("Open Error: $logfile");
	if ($in{'action'} ne "past") { $top = <IN>; }
	while (<IN>) {
		chomp;
		($no,$re,$dat,$name,$eml,$sub,$com,$url,$hos,$pw,$col,$ico,$tm,$sml) = split(/<>/);
		if ($no eq $hitnum || $re eq $hitnum) { 
			$no{$i}   = $no;
			$re{$i}   = $re;
			$dat{$i}  = $dat;
			$name{$i} = $name;
			$eml{$i}  = $eml;
			$sub{$i}  = $sub;
			$com{$i}  = $com;
			$url{$i}  = $url;
			$hos{$i}  = $hos;
			$pw{$i}   = $pw;
			$col{$i}  = $col;
			$ico{$i}  = $ico;
			$tm{$i}   = $tm;
			$sml{$i}  = $sml;
			$i++;
		}
	}
	close(IN);

	print "<p><table width=\"90%\" cellpadding=\"$cellpadding\" cellspacing=\"$cellspacing\" border=\"$border\" class=\"thread\">\n";
	local ($flg) = 0;
	# �\�[�g����
	$j = 0;
	foreach (sort { ($no{$a} <=> $no{$b}) } keys(%no)) {
		$j++;

		# �薼�̒���
		if (length($sub{$_}) > $sub_len*2) {
			$sub{$_} = substr($sub{$_},0,$sub_len*2);
			$sub{$_} .= "...";
		}

		$author{$_} = $name{$_};
		require $messagepl;
		$name{$_} = &emailscript($name{$_},$no{$_},$eml{$_},$sml{$_},$col{$_},$hos{$_});

		if ($re{$_}) {
			if (!$boardmode) { print "<hr noshade size=\"1\" width=\"85%\">\n"; }
			if (!$flg) {
					print "<div style=\"margin-left:$margin_left; margin-top:5px; margin-right:$margin_right;\">\n";
				$flg = 1;
			}
		}

		&messageform($no{$_},$re{$_},$dat{$_},$name{$_},$sub{$_},
		$com{$_},$url{$_},$pw{$_},$col{$_},$ico{$_},$author{$_},$tm{$_});

	}
	print "</div>\n</td></tr></table></p>\n";
}


1;

