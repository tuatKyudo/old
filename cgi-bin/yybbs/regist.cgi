#!/usr/local/bin/perl

#��������������������������������������������������������������������
#�� [ YY-BOARD ]
#�� regist.cgi - 2006/10/09
#�� Copyright (c) KentWeb
#�� webmaster@kent-web.com
#�� http://www.kent-web.com/
#�� 
#�� 
#�� �\�\�\�\�\�\�\�\�\�\�\�\�\�\[���ӎ���]�\�\�\�\�\�\�\�\�\�\�\�\�\�\
#�� 
#�� �{�X�N���v�g�ɂ��āAKENT WEB�T�|�[�g�f���ւ̎���͋֎~�ł��B
#�� ���p�K������Ȃ��ꍇ�ɂ͖{�����X�N���v�g�̎g�p����ؔF�߂܂���B
#�� 
#�� �\�\�\�\�\�\�\�\�\�\�\�\�\�\[���ӎ���]�\�\�\�\�\�\�\�\�\�\�\�\�\�\
#�� 
#�� 
#�� YY-BOARD Antispam Version Modified by isso.
#�� http://swanbay-web.hp.infoseek.co.jp/index.html
#��������������������������������������������������������������������

# �O���t�@�C���捞
require './init.cgi';
require $jcode;

# �J���[�f�[�^�t�@�C��
if (-e "$colorfile") {
	open(COL,"$colorfile");
	$boardmode = <COL>;
	close(COL);
} else {
	open(OUT,">>$colorfile");
	print OUT "0";
	close(OUT);
	$boardmode = 0;
}
unless(-e "$colordata") {
	&error("�J���[�f�[�^�t�@�C�� $colordata ������܂���B");
}

# �\�����[�h�ݒ�
if ($boardmode && -s "$colordata") { &read_color; }

#-------------------------------------------------
# ���C������
#-------------------------------------------------
&agent;
&decode;
&axsCheck;
($mode,$timecheck) = &previewcheck;

# ������
if ($clday) {
	my $last = (stat $logfile)[9];
	if (abs(time - $last) > $clday*24*3600) {
		&header;
		&pseudo;
		&autoclose;
	}
}

if ($mode eq "dele") { require $editlogpl; &dele; }
elsif ($mode eq "edit") { require $editlogpl; &edit; }
elsif ($mode eq "$writevalue" && $in{'pview'} ne "on") { &regist; }
elsif ($mode eq "$postvalue" && $in{'pview'} eq "on") { &regist; }
elsif ($mode eq "$writevalue" && $in{'pview'} eq "on") { &error("$spammsg"); }
elsif ($mode eq "previewmode") { &previewmode("$timecheck"); }
elsif ($in{'pass'} eq $pass && $mode eq "admin_repost") { &regist; }
elsif ($mode eq "regist" || $mode eq "write") { &message("���e�����𒆎~���܂����B"); }
&error("�s���ȏ����ł��B");

#-------------------------------------------------
#  �L���o�^
#-------------------------------------------------
sub regist {
	local($cnam,$ceml,$curl,$cpwd,$cico,$ccol,$csmail,$caikotoba,$cref) = &get_cookie;

	# ���Ԏ擾
	&get_time;

	# �t�H�[�����̓`�F�b�N
	@col = split(/\s+/, $color);
	if ($mode ne "admin_repost") { &formCheck; }

	# �Ǘ��ҍ��̃`�F�b�N
	my $acflag = 0;
	foreach (split(/\,/, $AdminName)) {
		if ($in{'name'} =~ /\Q$_\E/i) { $acflag=1; last; }
	}
	if ($adminchk && $acflag) { &error("$in{'name'}�𖼏�邱�Ƃ͂ł��܂���B"); }

	# �Ǘ��҃`�F�b�N
	my $aflag = 0;
	if ($in{'name'} eq $admin_id && $in{'pwd'} eq $pass) {
		$ccolor = $in{'color'}; @color = split(/\s+/, $color); $acol = $#color+1;
		$in{'color'} = $acol; $col[$acol] = $a_color;
		$in{'name'} = $a_name; $aflag = 1;
	}

	# ���e�L�[�`�F�b�N
	if ($regist_key && $mode ne "admin_repost") {
		require $regkeypl;

		if ($in{'regikey'} !~ /^\d{4}$/) {
			&error("���e�L�[�����͕s���ł��B<p>���e�t�H�[���ɖ߂��čēǍ��݌�A�w��̐�������͂��Ă�������");
		}

		# ���e�L�[�`�F�b�N
		# -1 : �L�[�s��v
		#  0 : �������ԃI�[�o�[
		#  1 : �L�[��v
		local($chk) = &registkey_chk($in{'regikey'}, $in{'str_crypt'});
		if ($chk == 0) {
			&error("���e�L�[���������Ԃ𒴉߂��܂����B<p>���e�t�H�[���ɖ߂��čēǍ��݌�A�w��̐������ē��͂��Ă�������");
		} elsif ($chk == -1) {
			&error("���e�L�[���s���ł��B<p>���e�t�H�[���ɖ߂��čēǍ��݌�A�w��̐�������͂��Ă�������");
		}
	}

	# ���O���J��
	open(DAT,"+< $logfile") || &error("Open Error: $logfile");
	eval "flock(DAT, 2);";
	my $top = <DAT>;

	# �L��NO����
	local($no,$ip,$tim) = split(/<>/, $top);
	$no++;

	# �A�����e�`�F�b�N
	my $flg = 0;
	if ($mode ne "admin_repost") {
		if ($regCtl == 1) {
			if ($addr eq $ip && $times - $tim < $wait) { $flg = 1; }
		} elsif ($regCtl == 2) {
			if ($times - $tim < $wait) { $flg = 1; }
		}
		if ($flg) {
			close(DAT);
			&error("���ݓ��e�������ł��B�������΂炭�����Ă��瓊�e�����肢���܂�");
		}
	}

	# ���s�E�_�u���N�I�[�g����
	if ($in{'pview'} eq "on") {
		$in{'comment'} =~ s/&lt;br&gt;/<br>/g;
		$in{'comment'} =~ s/&quot;/"/g;
	}

	# �d���`�F�b�N
	my $flg = 0;
	while (<DAT>) {
		my ($no2,$re,$dat,$nam,$eml,$sub,$com) = split(/<>/);

		if ($in{'name'} eq $nam && $in{'comment'} eq $com) {
			$flg = 1;
			last;
		}
	}
	if ($flg) {
		close(DAT);
		&error("�d�����e�̂��ߏ����𒆒f���܂���");
	}

	# �����߂�
	seek(DAT, 0, 0);
	$top = <DAT>;

	# �폜�L�[���Í���
	if ($mode ne "admin_repost") {
		if ($in{'pwd'} ne "") { $pwd = &encrypt($in{'pwd'}); }
	}

	# �X�p�����e�`�F�b�N
	($spam,$reason) = &spam_check($in{'name'},$in{'url2'},$in{"$bbscheckmode"},$in{'comment'},
	$in{'reno'},$in{'url'},$in{'email'},$in{'sub'},$in{'mail'},$in{"$formcheck"},$cnam,$in{'submit'},
	$in{'subject'},$in{'title'},$in{'theme'},$ENV{'HTTP_ACCEPT_LANGUAGE'},$ENV{'HTTP_USER_AGENT'});

	# �v���r���[���X�p�����O�̍폜
	if ($in{'pview'} eq "on" || $mode eq "admin_repost") {
		if ($spamlog) { &del_spamlog("$in{\"$bbscheckmode\"}","spam"); }
	}
	# �G���[���O�̍폜
	if ($errtime) { &del_spamlog("$in{\"$bbscheckmode\"}","error"); }

	# �X�p�����e����
	if ($spam && $mode ne "admin_repost") {
		close(DAT);
		# ���e���ۃ��O�̋L�^
		if ($spamlog && !$allowmode) { &write_spamlog("$reason","spam"); }
		if ($spamresult) {
			# �G���[�\��
			if ($spammsg) {
				if ($spamresult == 1)  { &error("$spammsg","1"); }
				else { sleep($spamresult); &error("$spammsg","1"); }
			}
		}
		# Internal Server Error
		&cgi_error;
	}

	# ��������
	if ($mode eq "admin_repost") {
		$date= $in{'date'};
		$host= $in{'host'};
		$pwd = $in{'pwd'};
		$times= $in{'tim'};
	}

	# ���e����
	if ($mode ne "admin_repost") {
		my $result = &post_check;
		if ($result) {
			close(DAT);
			&write_spamlog("$result","spam");
			&message("$denymsg");
		}
	}

	# �N�b�L�[���s
	if ($mode ne "admin_repost") {
		if ($aflag) {
			if ($no_email == 2) { $in{'email'} =~ s/\@/��/; }
			&set_cookie($admin_id,$in{'email'},$in{'url'},$in{'pwd'},
			$in{'icon'},$ccolor,$in{'smail'},$in{'aikotoba'},$in{'refmode'});
			if ($no_email == 2) { $in{'email'} =~ s/��/\@/; }
		} else {
			if ($no_email == 2) { $in{'email'} =~ s/\@/��/; }
			&set_cookie($in{'name'},$in{'email'},$in{'url'},$in{'pwd'},
			$in{'icon'},$in{'color'},$in{'smail'},$in{'aikotoba'},$in{'refmode'});
			if ($no_email == 2) { $in{'email'} =~ s/��/\@/; }
		}
	}

	# ���e����J����
	my (@lines,@spampost);
	if (!$aflag && $allowmode && $mode ne "admin_repost") {
		close(DAT);
		# ����J���O�t�@�C���ǂݍ���
		open(SPLOG,"$spamlogfile") || &error("���O�t�@�C�� $spamlogfile ������܂���B");
		@lines = <SPLOG>;
		close(SPLOG);

		# ��d���e�̃`�F�b�N
		my $flag = 0;
		foreach (@lines) {
			@spampost = split(/<>/);
			if ($in{'comment'} eq $spampost[6]) { $flag = 1; last; }
			# �A�����e�`�F�b�N
			if ($host eq $spampost[8] && $wait > $times - $spampost[12]) {
				&error("�������΂炭���Ԃ������Ă��瓊�e���ĉ�����");
			}
		}
		if ($flag) { &error("��d���e�͋֎~�ł�"); }

		&write_spamlog("$reason","spam");
		# ���[���ʒm
		if ($mailing == 1 && $in{'email'} ne $mailto) { &mail_to; }
		elsif ($mailing == 2) { &mail_to; }
		&message("$spammsg");
	}

	# sage
	if ($in{'sage'}) {
		$topsort = 0;
	}

	# �e�L���̏ꍇ
	if ($in{'reno'} eq "") {

		my $i = 0;
		my $stop = 0;
		while (<DAT>) {
			my ($no2,$reno2) = split(/<>/);
			$i++;
			if ($i > $max-1 && $reno2 eq "") { $stop = 1; }
			if (!$stop) { push(@new,$_); }
			elsif ($stop && $pastkey) { push(@data,$_); }
		}
		unshift(@new,"$no<><>$date<>$in{'name'}<>$in{'email'}<>$in{'sub'}<>$in{'comment'}<>$in{'url'}<>$host<>$pwd<>$col[$in{'color'}]<>$in{'icon'}<>$times<>$in{'smail'}<>\n");
		if ($mode ne "admin_repost") {
			unshift(@new,"$no<>$addr<>$times<>\n");
		} else {
			unshift(@new,"$no<>$ip<>$tim<>\n");
		}

		# �ߋ����O�X�V
		if (@data > 0) { &pastlog(@data); }

		# �X�V
		seek(DAT, 0, 0);
		print DAT @new;
		truncate(DAT, tell(DAT));
		close(DAT);

	# ���X�L���̏ꍇ�F�g�b�v�\�[�g����
	} elsif ($in{'reno'} && $topsort) {

		my ($f,$oyaChk,$match,@new,@tmp);
		while (<DAT>) {
			my ($no2,$reno2) = split(/<>/);

			if ($in{'reno'} == $no2) {
				if ($reno2) { $f++; last; }
				$oyaChk++;
				$match=1;
				push(@new,$_);

			} elsif ($in{'reno'} == $reno2) {
				push(@new,$_);

			} elsif ($match == 1 && $in{'reno'} != $reno2) {
				$match=2;
				push(@new,"$no<>$in{'reno'}<>$date<>$in{'name'}<>$in{'email'}<>$in{'sub'}<>$in{'comment'}<>$in{'url'}<>$host<>$pwd<>$col[$in{'color'}]<>$in{'icon'}<>$times<>$in{'smail'}<>\n");
				push(@tmp,$_);

			} else { push(@tmp,$_); }
		}
		if ($f) {
			close(DAT);
			close(DAT);&error("�s���ȕԐM�v���ł�");
		}
		if (!$oyaChk) {
			close(DAT);
			&error("�e�L�������݂��܂���");
		}

		if ($match == 1) {
			push(@new,"$no<>$in{'reno'}<>$date<>$in{'name'}<>$in{'email'}<>$in{'sub'}<>$in{'comment'}<>$in{'url'}<>$host<>$pwd<>$col[$in{'color'}]<>$in{'icon'}<>$times<>$in{'smail'}<>\n");
		}
		push(@new,@tmp);

		# �X�V
		unshift(@new,"$no<>$addr<>$times<>\n");
		seek(DAT, 0, 0);
		print DAT @new;
		truncate(DAT, tell(DAT));
		close(DAT);

	# ���X�L���̏ꍇ�F�g�b�v�\�[�g�Ȃ�
	} else {

		my ($f,$oyaChk,$match,@new);
		while (<DAT>) {
			my ($no2,$reno2) = split(/<>/);

			if ($in{'reno'} == $no2) { $oyaChk++; }
			if ($match == 0 && $in{'reno'} == $no2) {
				if ($reno2) { $f++; last; }
				$match = 1;

			} elsif ($match == 1 && $in{'reno'} != $reno2) {
				$match = 2;
				push(@new,"$no<>$in{'reno'}<>$date<>$in{'name'}<>$in{'email'}<>$in{'sub'}<>$in{'comment'}<>$in{'url'}<>$host<>$pwd<>$col[$in{'color'}]<>$in{'icon'}<>$times<>$in{'smail'}<>\n");
			}
			push(@new,$_);
		}
		if ($f) {
			close(DAT);
			&error("�s���ȕԐM�v���ł�");
		}
		if (!$oyaChk) {
			close(DAT);
			&error("�e�L�������݂��܂���");
		}

		if ($match == 1) {
			push(@new,"$no<>$in{'reno'}<>$date<>$in{'name'}<>$in{'email'}<>$in{'sub'}<>$in{'comment'}<>$in{'url'}<>$host<>$pwd<>$col[$in{'color'}]<>$in{'icon'}<>\n");
		}

		# �X�V
		unshift(@new,"$no<>$addr<>$times<>\n");
		seek(DAT, 0, 0);
		print DAT @new;
		truncate(DAT, tell(DAT));
		close(DAT);
	}

	if ($mode ne "admin_repost") {
		# ���[������
		if ($mailing == 1 && $in{'email'} ne $mailto) { &mail_to; }
		elsif ($mailing == 2) { &mail_to; }
	}

	# �����[�h
	if ($location) {
		if ($ENV{'PERLXS'} eq "PerlIS") {
			print "HTTP/1.0 302 Temporary Redirection\r\n";
			print "content-type: text/html\n";
		}
		print "Location: $location?list=$in{'list'}\n\n";
		exit;

	} else {
		&message('���e�͐���ɏ�������܂���');
	}
}

#-------------------------------------------------
#  ���͊m�F
#-------------------------------------------------
sub formCheck {
	local($task) = @_;
	local($ref);

	# POST����
	if ($postonly && !$post_flag) { &error("�s���ȃA�N�Z�X�ł�"); }

	# ���e��
	if ($task ne "edit") {
		# ���T�C�g����̃A�N�Z�X�r��
		if ($baseUrl) {
			$ref = $ENV{'HTTP_REFERER'};
			$ref =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("H2", $1)/eg;
			$baseUrl =~ s/(\W)/\\$1/g;
			if ($ref && $ref !~ /$baseUrl/i) { &error("�s���ȃA�N�Z�X�ł�"); }
		}

		# �g���I�v�V�����`�F�b�N
		&option_check($in{'pwd'},$in{'email'},$in{'message'},$in{'url'});
		if ($in{'email'} && $in{'email'} =~ /��/) { $in{'email'} =~ s/��/\@/; }

		if ($aikotoba) {
			if ($in{'aikotoba'} ne $aikotoba) { &error("�������t���s���ł�"); }
		}
	}

	# ���O�ƃR�����g�͕K�{
	if ($in{'name'} eq "") { &error("���O�����͂���Ă��܂���"); }
	if ($in{'comment'} eq "") { &error("�R�����g�����͂���Ă��܂���"); }
	if (!$in{'email'}) { $in{'smail'} = 0; }
	if ($in_email && $in{'email'} !~ /^[\w\.\-]+\@[\w\.\-]+\.[a-zA-Z]{2,6}$/) {
		&error("�d���[���̓��͓��e������������܂���");
	}
	if (!$in_email && $in{'email'}) {
		if ($in{'email'} !~ /^[\w\.\-]+\@[\w\.\-]+\.[a-zA-Z]{2,6}$/) {
			&error("�d���[���̓��͓��e������������܂���");
		}
	}

	if ($iconMode) {
		@ico1 = split(/\s+/, $ico1);
		@ico2 = split(/\s+/, $ico2);
		if ($my_icon) { push(@ico1,$my_gif); }
		if ($in{'icon'} =~ /\D/ || $in{'icon'} < 0 || $in{'icon'} > @ico1) {
			&error("�A�C�R����񂪕s���ł�");
		}
		$in{'icon'} = $ico1[$in{'icon'}];

		# �Ǘ��A�C�R���`�F�b�N
		if ($my_icon && $in{'icon'} eq $my_gif && $in{'pwd'} ne $pass) {
			&error("�Ǘ��p�A�C�R���͊Ǘ��Ґ�p�ł�");
		}
	}

	@col = split(/\s+/, $color);
	if ($in{'color'} =~ /\D/ || $in{'color'} < 0 || $in{'color'} > @col) {
		&error("�����F��񂪕s���ł�");
	}

	# email�`�F�b�N
	if ($in{'email'}) {
		my $atmark = $in{'email'} =~ s/\@/\@/g;
		if ($atmark != 1) {
			&error("�d���[���̓��͂��s���ł�");
		}
	}

	# URL
	if ($in{'url'} && $in{'url'} !~ /^https?\:\/\//i) { &error("URL�̓��͂��s���ł�"); }
	if ($in{'url'} eq "http://") { $in{'url'} = ""; }

	# �@��ˑ������`�F�b�N
	$pdcnam = &find_mdc( $in{'name'}, $pdch, $pdcf );
	if($pdcnam) { &error("$pdcerror�w&nbsp;$pdcnam&nbsp;�x"); }
	$pdcsub = &find_mdc( $in{'sub'}, $pdch, $pdcf );
	if($pdcsub) { &error("$pdcerror�w&nbsp;$pdcsub&nbsp;�x"); }
	$pdcmsg = &find_mdc( $in{'comment'}, $pdch, $pdcf );
	if($pdcmsg) { &error("$pdcerror<br><br><table border=1><tr><td>$pdcmsg</td></tr></table>"); }

	# �^�C�g���`�F�b�N
	if (!$in{'sub'}) {
		if ($suberror) { &error("�^�C�g�������͂���Ă��܂���"); } else { $in{'sub'} = "����"; } 
	} elsif ($suberror == 2) {
		if ($in{'sub'} !~ /[^0-9]/ || $in{'sub'} =~ /http\:\/\//i) { &error("�^�C�g�����s���ł�"); }
	}

	# ���p�����E���p���������e�̋֎~
	$cflg = 0; $rowa = 0; $rowb = 0;
	$message = $in{'comment'};
	$message =~ s/&lt;br&gt;/<br>/g;
	@message = split(/<br>/i,$message);
	foreach(@message){
		if ($_ =~ /^>/ || $_ =~ /^&gt;/) {
			# ���p���������J�E���g
			$rowa = $rowa+length($_); next;
			# ���b�Z�[�W���������J�E���g
		} elsif($_) { $rowb = $rowb+length($_); $cflg = 1;} 
	}
	if (!$cflg) { &error("���p���������邩�R�����g������܂���"); }
	if ($mode ne "admin_repost" && $rrate) {
		if ($rowa/$rowb >= $rrate) { &error("���p�������������܂�"); }
	}

	# ����J�`�F�b�N
	if ($in{'smail'}) {
		if ($in{'smail'} ne "1") { &error("�I��������������܂���B");}
	}
}

#-------------------------------------------------
#  �@��ˑ��������o  
#-------------------------------------------------
# �@��ˑ��������o�{�n�C���C�g�\���ǉ��֐�
# Check platform dependent characters / Thanks to carmine
# [Usage] $result = &find_mdc( $buf, '<font color="red">', '</font>' );
sub find_mdc {
	local( $buf, $prefix, $postfix ) = @_;
	local( $len, $c1, $c2, $o1, $o2, $i, $k, $pdc, $result );

	$k = 0;
	$pdc = 0;
	$result = "";
	$len = length( $buf );
	for( $i = 0; $i < $len; ++$i ){
		if( $k ){
			$k = 0;
			$c2 = substr( $buf, $i, 1 );
			$o2 = ord( $c2 );
			if( ( $o1 >= 0x85 && $o1 <= 0x88 ) && ( $o2 >= 0x40 && $o2 <= 0x9e ) ){
				$result .= $prefix . $c1 . $c2 . $postfix;
				$pdc = 1;
			} else {
				$result .= $c1 . $c2;
			}
			$k = 0;
		} else {
			$c1 = substr( $buf, $i, 1 );
			$o1 = ord( $c1 );
			if( ( $o1 > 0x80 && $o1 <= 0x9F ) || ( $o1 >= 0xE0 && $o1 <= 0xFC ) ){
				$k = 1;
			} else {
				$result .= $c1;
			}
		}
	}
	if ($pdc) { return $result; } else {return $pdc; }
}

#-------------------------------------------------
#  ���[�����M
#-------------------------------------------------
sub mail_to {
	# �L���̉��s�E�^�O�𕜌�
	my $com  = $in{'comment'};
	$com =~ s/<br>/\n/g;
	my $ptn = 'https?\:[\w\.\~\-\/\?\&\+\=\:\@\%\;\#\%]+';
	$com =~ s/<a href="$ptn" target="_blank">($ptn)<\/a>/$1/go;
	$com =~ s/&lt;/��/g;
	$com =~ s/&gt;/��/g;
	$com =~ s/&quot;/�h/g;
	$com =~ s/&amp;/��/g;

	# ���[���{�����`
	my $agent = &escape($ENV{'HTTP_USER_AGENT'});
	my $mbody = <<EOM;
���e�����F$date
�z�X�g���F$host
�u���E�U�F$agent

���e�Җ��F$in{'name'}
�d���[���F$in{'email'}
�Q�Ɛ�  �F$in{'url'}
�^�C�g���F$in{'sub'}

$com
EOM

	# �薼��BASE64��
	my $msub = &base64("$title (No.$no)");

	# �R�[�h�ϊ�
	&jcode::convert(\$mbody, 'jis', 'sjis');

	# ���[���A�h���X���Ȃ��ꍇ�͊Ǘ��҃A�h���X�ɒu������
	 my $email = $in{'email'};
	 if ($in{'email'} eq "") { $email = $mailto; }

	open(MAIL,"| $sendmail -t -i") || &error("���[�����M���s");
	print MAIL "To: $mailto\n";
	print MAIL "From: $email\n";
	print MAIL "Subject: $msub\n";
	print MAIL "MIME-Version: 1.0\n";
	print MAIL "Content-type: text/plain; charset=iso-2022-jp\n";
	print MAIL "Content-Transfer-Encoding: 7bit\n";
	print MAIL "X-Mailer: $ver\n\n";
	print MAIL "--------------------------------------------------------\n";
	print MAIL "$mbody\n";
	print MAIL "--------------------------------------------------------\n";
	close(MAIL);
}

#-------------------------------------------------
#  BASE64�ϊ�
#-------------------------------------------------
#		�Ƃقق�WWW����Ō��J����Ă��郋�[�`����
#		�Q�l�ɂ��܂����B( http://tohoho.wakusei.ne.jp/ )
sub base64 {
	my $sub = shift;
	&jcode::convert(\$sub, 'jis', 'sjis');

	$sub =~ s/\x1b\x28\x42/\x1b\x28\x4a/g;
	$sub = "=?iso-2022-jp?B?" . &b64enc($sub) . "?=";
	$sub;
}
sub b64enc {
	local($ch)="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
	local($x, $y, $z, $i);
	$x = unpack("B*", $_[0]);
	for ($i = 0; $y=substr($x,$i,6); $i+=6) {
		$z .= substr($ch, ord(pack("B*", "00" . $y)), 1);
		if (length($y) == 2) {
			$z .= "==";
		} elsif (length($y) == 4) {
			$z .= "=";
		}
	}
	$z;
}

#-------------------------------------------------
#  �ߋ����O����
#-------------------------------------------------
sub pastlog {
	local(@data) = @_;

	# �ߋ����ONo�t�@�C��
	open(NO,"+< $nofile") || &error("Open Error: $nofile");
	eval "flock(NO, 2)";
	my $count = <NO>;

	# �ߋ����O��`
	my $pastfile = sprintf("%s/%04d.cgi", $pastdir,$count);

	# �ߋ����O�I�[�v��
	my $i = 0;
	my ($flg, @past);
	open(PF,"+< $pastfile") || &error("Open Error: $pastfile");
	eval "flock(PF, 2)";
	while (<PF>) {
		$i++;
		push(@past,$_);
		if ($i >= $pastmax) { $flg++; last; }
	}

	# �K��̍s�����I�[�o�[����Ǝ��t�@�C������������
	if ($flg) {

		# �J�E���g�t�@�C���X�V
		seek(NO, 0, 0);
		print NO ++$count;
		truncate(NO, tell(NO));

		close(PF);

		# �V�ߋ����O
		$pastfile = sprintf("%s/%04d.cgi", $pastdir,$count);
		@past = @data;

		open(PF,"> $pastfile") || &error("Open Error: $pastfile");
		print PF @past;
		close(PF);

	} else {
		unshift(@past,@data);

		# �ߋ����O�X�V
		seek(PF, 0, 0);
		print PF @past;
		truncate(PF, tell(PF));
		close(PF);
	}

	close(NO);

	# �V�K�����̏ꍇ�p�[�~�b�V�����ύX
	if ($flg) { chmod(0666, $pastfile); }
}

#-------------------------------------------------
#  �֎~���[�h�`�F�b�N
#-------------------------------------------------
sub no_wd {
	local($flg);
	foreach ( split(/,/, $no_wd) ) {
		if (index("$in{'name'} $in{'sub'} $in{'comment'}",$_) >= 0) {
			$flg = 1; last;
		}
	}
	if ($flg) { &error("�֎~���[�h���܂܂�Ă��܂�"); }
}

#-------------------------------------------------
#  ���{��`�F�b�N
#-------------------------------------------------
sub jp_wd {
	local($sub, $com, $mat1, $mat2, $code1, $code2);
	$sub = $in{'sub'};
	$com = $in{'comment'};
	if ($sub) {
		($mat1, $code1) = &jcode'getcode(*sub);
	}
	($mat2, $code2) = &jcode'getcode(*com);
	if ($code1 ne 'sjis' && $code2 ne 'sjis') {
		&error("�薼���̓R�����g�ɓ��{�ꂪ�܂܂�Ă��܂���");
	}
}

#-------------------------------------------------
#  URL���`�F�b�N
#-------------------------------------------------
sub urlnum {
	local($com) = $in{'comment'};
	local($num) = ($com =~ s|(https?://)|$1|ig);
	if ($num > $urlnum) {
		&error("�R�����g����URL�A�h���X�͍ő�$urlnum�܂łł�");
	}
}

#-------------------------------------------------
#  �X�p���g���I�v�V�����`�F�b�N
#-------------------------------------------------
sub option_check {
	my ($pw,$em,$cm,$ur) = @_;

	# �폜�L�[���`�F�b�N
	my $flag = 0;
	if ($ng_pass && $pw) {
		if ($pw =~ /\s/ || $pw eq reverse($pw)) {
			$flag = 1;
		}
	}
	if ($flag) {
		&error("�폜�L�[���s���ł��B");
	}

	# ���[���A�h���X���`�F�b�N
	if ($no_email == 1 && $em) {
		&error("���[���A�h���X�͓��͋֎~�ł��B");
	}
	if ($no_email == 2 && $em && $em !~ /^[\w\.\-]+��[\w\.\-]+\.[a-zA-Z]{2,6}$/) {
		&error("�A�b�g�}�[�N �� �͑S�p�œ��͂��ĉ������B"); 
	}

	# URL�̒��ڏ������݂��`�F�b�N
	if ($comment_url) { 
		my $ulnum = ($cm =~ s/http/http/ig);
		if ($ulnum) {
			&error("�t�q�k�͐擪�̂��𔲂��ď�������ŉ������B");
		}
	}

	# URL�]���E�Z�kURL���`�F�b�N
	my $shorturlcheck = 0;
	if ($shorturl) { 
		if ($cm =~ /https?\:\/\/[\w\-]{1,10}?\.[\w\-]{2,5}?\//i || 
			$ur =~ /https?\:\/\/[\w\-]{1,10}?\.[\w\-]{2,5}?\//i) {
			my $html = $';
			if ($html =~ /^[\w\?]+?/)  {
				if ($html !~ /^index\.htm/i) {
					$shorturlcheck = 1;
				}
			}
		}
		if (!$shorturlcheck) {
			if ($cm =~ /https?\:\/\/([\w\-]{1,5}\.)?(\d+)\.[a-z]{2,4}\/?/i || 
				$ur =~ /https?\:\/\/([\w\-]{1,5}\.)?(\d+)\.[a-z]{2,4}\/?/i)
				{ $shorturlcheck = 2; }
		}
		if ($shorturlcheck) {
			&error("URL�̋L�ڂ͋֎~����Ă��܂��B");
		}
	}
}

#-------------------------------------------------
#  �X�p���`�F�b�N
#-------------------------------------------------
sub spam_check{
	my ($na,$u2,$bt,$cm,$re,$ur,$em,$sb,$ad,$fc,$cn,$smt,$sb2,$sb3,$sb4,$lng,$ua) = @_;
	my $spam = 0;
	my $reason = "���J���҂�";
	my $tcheck = abs(time - $bt);

	if (!$spam) {
		if($ipcheckmode) {
			my $enadr = &encode_addr($addr);
			if ($ad ne $enadr) {
				$spam = 1;
				$reason = "�v���O�������e(IP�s��v)";
			}
		} else {
			if ($ad =~ /\@/) {
				$spam = 1;
				$reason = "�v���O�������e(IP�f�[�^�s��)";
			}
		}
	}

	if (!$spam) {
		if (!$cn || !$cookiecheck) {
			if ($maxtime && $tcheck > $maxtime) {
				$spam = 1;
				$reason = "�v���O�������e(���e�܂�$tcheck�b)";
			}
		}
	}

	# �g�я��O
	if ($keitaicheck == 1 && $keitai ne 'p') { $spam = 0; }

	if (!$spam) {
		if (!$smt) {
			$spam = 1;
			$reason = "�v���O�������e(���e�{�^����g�p)";
		}
	}

	if (!$spam) {
		if ($u2 || $sb2 || $sb3 || $sb4) {
			$spam = 1;
			$reason = "�v���O�������e(��u���E�U)";
		}
	}

	if (!$spam) {
		if (!$bt || !$fc || !$ad) {
			$spam = 1;
			$reason = "�v���O�������e(��t�H�[�����e)";
		}
	}

	if (!$spam) {
		if ($mintime && $tcheck < $mintime) {
			if ($cn && $cookiecheck) {
				&error("�������܂����A��x�߂��Ă���ē��e���Ă��������B");
			}
			$spam = 1;
			$reason = "�v���O�������e(���e�܂�$tcheck�b)";
		}
	}

	# �g�я��OII
	if (!$keitaicheck && $keitai ne 'p') { $spam = 0; }

	# �g�т����URL�L���`�F�b�N
	if (!$spam) {
		if($keitaiurl && $keitai ne 'p') {
			if ($cm =~ /http/i || $ur) {
				&error("URL�͏������܂Ȃ��ł��������B");
			}
		}
	}

	if (!$spam) {
		if ($em && $em =~ /https?\:\/\//) {
			$spam = 1;
			$reason = "�v���O�������e(email/URL�s��)";
		}
	}

	if (!$spam) {
		if ($ur && $ur =~ /^[\w\.\-]+\@[\w\.\-]+\.[a-zA-Z]{2,6}$/) {
			$spam = 1;
			$reason = "�v���O�������e(email/URL�s��)";
		}
	}

	if (!$spam) {
		if ($minmsg) {
			if (length($cm)*2 < length($na)) {
				&error("�R�����g�E���b�Z�[�W���Z�����܂��B");
			}
		}
		if ($namelen && length($na) >= $namelen) {
			&error("���Ȃ܂����s�K�؂ł��B");
		}
		if ($cm eq $na) {
			&error("�R�����g�E���b�Z�[�W���e���s�K�؂ł��B");
		}
	}

	if (!$spam) {
		if ($na =~ /https?\:\/\//i) {
			$spam = 1;
			$reason = "�v���O�������e(name/comment�s��)";
		}
	}

	# �X�p�����e�`�F�b�N(����URL�L�q�Ή�)
	if (!$spam) {
		my $ulnum = ($cm =~ s/http/http/ig);
		if ($spamurlnum && ($ulnum >= $spamurlnum)) {
			$spam = 1;
			$reason = "URL�̏������݂�$ulnum��";
		}
	}

	# URL�ȊO�̕��������`�F�b�N
	if (!$spam) {
		if ($characheck) {
			if ($cm =~ /(https?\:\/\/[\w\.\~\-\/\?\&\=\;\#\:\%\+\@\,]+)/ || $ur) {
				my $charamsg = $cm;
				$charamsg =~ s/(https?\:\/\/[\w\.\~\-\/\?\&\=\;\#\:\%\+\@\,]+)//g;
				$charamsg =~ s/[\s\n\r\t]//g;
				$charamsg =~ s/<br>//ig;
				$msgnum = length($charamsg);
				if ($msgnum < $characheck) {
					$spam = 1;
					$reason = "�R�����g�̕�������$msgnum�o�C�g�Ə��Ȃ�";
				}
			}
		}
	}

	# ���{�ꕶ�`�F�b�N
	if (!$spam) {
		if ($asciicheck) {
			if ($cm !~ /(\x82[\x9F-\xF2])|(\x83[\x40-\x96])/) {
				$spam = 1;
				$reason = "�R�����g�ɓ��{��(�Ђ炪��/�J�^�J�i)���Ȃ�";
			} else {
				my $flag = 0;
				foreach (@period ) {
					if ($cm =~ /$_/) {
						$flag = 1;
						last;
					}
				}
				if (!$flag) {
					$spam = 1;
					$reason = "�R�����g�ɋ�Ǔ_���Ȃ�";
				}
			}
		}
	}

	if (!$spam) {
		if (-e $spamdata) {
			if ($spamdatacheck || !$re) {
				# �֎~URL�f�[�^�����[�h
				open(SPAM,"$spamdata") || &error("Open Error : $spamdata");
				eval { flock(SPAM, 1); };
				my $SPM = <SPAM>;
				close(SPAM);
				# �֎~URL�̏������݂��`�F�b�N
				foreach (split(/\,/, $SPM)) {
					if(length($_) > 1) {
						if ($cm =~ /\Q$_\E/i) {
							$spam = 1;
							$reason = "���O/�R�����g���ɋ֎~���$_���܂ޓ��e";
							last;
						}
						if (!$spam && $na =~ /\Q$_\E/i) {
							$spam = 1;
							$reason = "���O/�R�����g���ɋ֎~���$_���܂ޓ��e";
							last;
						}
						if (!$spam && $ur =~ /\Q$_\E/i) {
							$spam = 1;
							$reason = "URL�ɋ֎~���$_���܂ޓ��e";
							last;
						}
						if (!$spam && $ngmail && $em =~ /\Q$_\E/i) {
							$spam = 1;
							$reason = "���[���A�h���X�ɋ֎~���$_���܂ޓ��e";
							last;
						}
						if (!$spam && $ngtitle && $sb =~ /\Q$_\E/i) {
							$spam = 1;
							$reason = "�^�C�g���ɋ֎~���$_���܂ޓ��e";
							last;
						}
					}
				}
			}
		}
	}

	if (!$spam) {
		if ($urlcheck) {
			if ($urlcheck eq 2 || !$re) {
				# URL�̃R�����g�ւ̏d���������݂��`�F�b�N
				if($ur) {
					$ur =~ s/\/$//;
					if ($cm =~ /\Q$ur\E/i) {
						if ($' !~ /(^\/?[\w\?]+?)/)  {
							$spam = 1;
							$reason = "�R�����g����URL���Ɠ���URL���܂ޓ��e";
						}
					}
				}
			}
		}
	}

	if (!$spam) {
		if (-e $spamip) {
			use Socket;
			my ($ip,$ngip,$dm,@dm);
			# �֎~URL�f�[�^�����[�h
			open(IP,"$spamip") || &error("Open Error : $spamip");
			eval { flock(IP, 1); };
			my $ipdata = <IP>;
			close(IP);
			# URL��
			$ur =~ s/\/$//g;
			$ur =~ s/https?\:\/\///g;
			if ($ur =~ /[\w\-]{2,}?\.[\w\.\~\-\?\&\=\+\@\;\#\:\%\,]{2,}/) {
				eval { $ip = inet_ntoa(inet_aton($&)); };
				foreach $ngip (split(/\,/, $ipdata)){
					if ($ip =~ /^$ngip/) {
						$spam = 1;
						$reason = "URL���ɋ֎~URL($ur)";
						last;
					}
				}
			}
			if (!$spam) {
				# �{��
				@dm = $cm =~ /[-_a-z0-9]{3,}\.[-_\.a-z0-9]{2,}/g;
				foreach $dm (@dm){
					eval { $ip = inet_ntoa(inet_aton($dm)); };
					foreach $ngip (split(/\,/, $ipdata)){
						if ($ip =~ /^$ngip/) {
							$spam = 1;
							$reason = "�R�����g���ɋ֎~URL($dm)";
							last;
						}
					}
				}
			}
		}
	}

	return ($spam,$reason);
}

#-------------------------------------------------
#  �G���[/�X�p�����O�폜
#-------------------------------------------------
sub del_spamlog {
	my ($checktime,$job) = @_;
	my $file = $spamlogfile;
	if ($job eq "error") {
		$file = $er_log;
	}
	my @new = ();
	open(DATA,"+<$file");
	eval { flock(DATA, 2); };
	while (<DATA>) {
		my ($no,$reno,$date,$name,$email,$sub,$msg,$url,$host,$pwd,$color,$icon,$tim,$sml,
		$reason,$fcheck,$referer,$useragent,$times) = split(/<>/);
		if ($fcheck ne $checktime) {
			push(@new,"$_");
		}
	}
	seek(DATA, 0, 0);
	print DATA @new;
	truncate(DATA, tell(DATA));
	close(DATA);
}

#-------------------------------------------------
#  �v���r���[�`�F�b�N
#-------------------------------------------------
sub previewcheck {
	$in{"$bbscheckmode"} = &decode_bbsmode($in{"$bbscheckmode"});
	if ($mode eq "$writevalue") {
		if ($previewmax || $previewmin) {
			if ($in{'pview'} ne "on") {
				$timecheck = abs(time - $in{"$bbscheckmode"});
				if ($timecheck <= $maxtime) {
					if ($previewmax) {
						if ($timecheck > $previewmax) {
							$mode = "previewmode";
						}
					}
				}
				if ($timecheck >= $mintime) {
					if ($timecheck < $previewmin) {
						$mode = "previewmode";
					}
				}
			}
		}
	}
	return ($mode,$timecheck);
}

#-------------------------------------------------
#  �v���r���[���
#-------------------------------------------------
sub previewmode {
	my $timecheck = shift;

	# �`�F�b�N
	&formCheck;

	# �v���r���[���O�̋L�^
	my $writelog = 0;
	if ($spamlog) {
		if ($spamlog == 2) {
			# �Ђ炪�Ȃ��܂ޏꍇ�̂݋L�^
			if ($in{'comment'} =~ /(\x82[\x9F-\xF2])/) {
				$writelog = 1;
			}
		} else {
			$writelog = 1;
		}
	}
	if ($writelog) {
		&write_spamlog("�v���r���[�\\����ɖ����e ($timecheck�b)","spam");
	}

	# �G���R�[�h����
	$in{"$bbscheckmode"} = &encode_bbsmode($in{"$bbscheckmode"});

	my $iflag = 0;
	my $i = 0;
	# �Ǘ��҃A�C�R��
	my @ico1 = split(/\s+/, $ico1);
	if ($my_icon) { push(@ico1,$my_gif); }
	# �A�C�R��
	foreach(@ico1) {
		if ($in{'icon'} =~ /$_/) {
			$iflag = 1; $in{'icon'} = $i; last;
		}
		$i++;
	}
	if(!$iflag) { $in{'icon'} = 0; }

	my $cflag = 0;
	my $j = 0;
	foreach(split(/\s+/, $color)) {
		if ($in{'color'} =~ /\Q$_\E/) {
			$cflag = 1; $col = $j; last;
		}
		$j++;
	}
	if(!$cflag) { $col = 0; }

	# URL
	if ($in{'url'} eq "http://") { $in{'url'} = ""; }

	&header;
	print <<EOM;
<form action="$registcgi" method="$method">
<input type="hidden" name="$bbscheckmode" value="$in{$bbscheckmode}">
<!--//
<input type="hidden" name="mode" value="write">
//-->
<input type="hidden" name="pwd" value="$in{'pwd'}">
<input type="hidden" name="name" value="$in{'name'}">
<input type="hidden" name="mail" value="$in{'mail'}">
<input type="hidden" name="email" value="$in{'email'}">
<input type="hidden" name="url" value="$in{'url'}">
<input type="hidden" name="sub" value="$in{'sub'}">
<input type="hidden" name="reno" value="$in{'reno'}">
<input type="hidden" name="icon" value="$in{'icon'}">
<input type="hidden" name="comment" value="$in{'comment'}">
<input type="hidden" name="color" value="$in{'color'}">
<input type="hidden" name="list" value="$in{'list'}">
<input type="hidden" name="num" value="$in{'num'}">
<input type="hidden" name="pview" value="on">
<input type="hidden" name="smail" value="$in{'smail'}">
<input type="hidden" name="sage" value="$in{'sage'}">
<input type="hidden" name="$formcheck" value="$in{$formcheck}">
<input type="hidden" name="aikotoba" value="$in{'aikotoba'}">
<input type="hidden" name="refmode" value="$in{'refmode'}">
<input type="hidden" name="regikey" value="$in{'regikey'}">
<input type="hidden" name="str_crypt" value="$in{'str_crypt'}">
EOM
	$in{'name'} =~ s/"/&quot;/g;
	$in{'sub'}  =~ s/"/&quot;/g;
	$in{'comment'} =~ s/"/&quot;/g;

	# ���W�I�{�^���I��
	my ($cnam,$ceml,$curl,$cpwd,$cico,$ccol,$csmail,$caikotoba,$cref) = &get_cookie;
	my $cm = $in{'comment'};
	my $ur = $in{'url'};
	my $em = $in{'email'};
	my $pflg = 0;

	# ���{��`�F�b�N
	my $checked0 = "";
	my $checked1 = "checked";
	my $checked2 = "";
	if ($cm =~ /(\x82[\x9F-\xF2])/) {
		$checked0 = "checked"; $checked1 = ""; $checked2 = "";

		# ��Ǔ_�`�F�b�N
		foreach (@period ) { if ($cm =~ /$_/) {$pflg = 1; last;} }
		if (!$pflg) { $checked0 = ""; $checked1 = ""; $checked2 = ""; }

		# URL�d���`�F�b�N
		$ur =~ s/\/$//;
		$em =~ s/\/$//;
		if (($ur && $cm =~ /\Q$ur\E/i) ||
			($em && $cm =~ /\Q$em\E/i)) {
			if ($' !~ /(^\/?[\w\?]+?)/)  {
				$checked0 = ""; $checked1 = ""; $checked2 = "checked";
			}
		}

		# URL�����̓`�F�b�N
		if ($ur)  {
			if (!$curl)  {
				$checked0 = ""; $checked1 = ""; $checked2 = "checked";
			}
		}

		# �R�����g��URL�`�F�b�N
		my $urlcnt = ($cm =~ s/http/http/ig);
		if ($urlcnt)  {
			if (!$cnam)  {
				$checked0 = ""; $checked1 = ""; $checked2 = "checked";
			}
		}
	}

	if ($keitai eq 'p') {
		print <<EOM;
<div align="center">
<h1 style="color:#ff0000; background-color:#ffffff; border-top-style:solid; border-bottom-style:solid; border-color:#ff0000; border-width:1; padding-top: 5px; padding-bottom: 5px;">���e�͂܂��������Ă���܂���B</h1>
<br>
�� ���e���m�F���A<b style="color:#ff0000">���e����</b>���`�F�b�N���ē��e�����s���ĉ������B<br>
<br>
<table border="1" width="90%" cellspacing="0" cellpadding="10">
<tr><td bgcolor="$tblcol">
<table>
<tr>
  <td><b>�����O</b></td>
  <td>$in{'name'}</td>
</tr>
<tr>
  <td><b>�d���[��</b></td>
  <td>$in{'email'}</td>
</tr>
<tr>
  <td><b>�^�C�g��</b></td>
  <td>$in{'sub'}</td>
</tr>
<tr>
  <td><b>�t�q�k</b></td>
  <td>$in{'url'}</td>
</tr>
<tr>
  <td><b>���b�Z�[�W</b></td>
  <td></td>
</tr>
</table>
<blockquote>
<table cellspacing="10">
<tr>
<td valign="top">$in{'comment'}</td>
</tr></blockquote>
</table>
</table>
<p>
<table cellpadding="5">
<tr>
  <td colspan="2">
  <script type="text/javascript">
  <!-- //
  fcheck("me='mode' va","<inpu","t type='radio' na","lue='$postvalue' class='radio' $checked0>");
  // -->
  </script>
  <noscript><input type="radio" name="mode" value="$postvalue"></noscript>
  <b style="color:#ff0000">���e����</b>
  &nbsp;&nbsp;&nbsp;
  <input type="radio" name="mode" value="regist" class="radio" $checked1><small>���e�L�����Z��</small>
  &nbsp;&nbsp;&nbsp;
  <input type="radio" name="mode" value="write" class="radio" $checked2><small>���e���~</small>
  </td>
</tr>
<tr>
  <td><div align="right">
   <input type="submit" name="submit" value="   ��    �s   " class="post">
   </form></div></td>
   <td><form><div align="left">
     <input type="button" value="�O��ʂɖ߂�" onclick="history.back()">
     </div></form>
  </td>
</tr>
</table>
</form>
</div>
</body>
</html>
EOM
	  } else {
		print <<EOM;
�� ���e���m�F���A���e�����s���ĉ������B
<hr>
���Ȃ܂�: 
<b style='color:#0000FF'>$in{'name'}</b><br>
�薼: 
<b style='color:#0000FF'>$in{'sub'}</b><br>
�d���[��: 
<b style='color:#0000FF'>$in{'email'}</b><br>
�R�����g<br>
<b style='color:#0000FF'>$in{'comment'}</b><br>
<hr>
<input type="radio" name="mode" value="$postvalue" $checked0>���e����
<br>
<input type="radio" name="mode" value="regist"s $checked1><small>���e����߂�</small>
<br>
<input type="submit" name="submit" value="   ��    �s   " class="post">
</form>
<form>
<input type="button" value="�O��ʂɖ߂�" onclick="history.back()">
EOM
	}
	exit;
}

#-------------------------------------------------
#  ���e����
#-------------------------------------------------
sub post_check {
	my $result = "";
	my $flg = 0;

	# IP�`�F�b�N
	foreach ( split(/\,/, $daddr) ) {
		s/\./\\\./g;
		s/\*/\.\*/g;
		if ($addr =~ /^$_/i) {
			$flg = 1;
			$result = "���e����IP�A�h���X����̓��e";
			last;
		}
	}
	if (!$flg) {
		# host�`�F�b�N
		foreach ( split(/\,/, $dhost) ) {
			s/\./\\\./g;
			s/\*/\.\*/g;
			if ($host =~ /$_$/i) {
				$flg = 1;
				$result = "���e�����z�X�g�A�h���X����̓��e";
				last;
			}
		}
	}
	return $result;
}

__END__

