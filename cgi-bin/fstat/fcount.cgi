#!/usr/bin/perl
require 5.004;   # �{�v���O������(���Ȃ��Ƃ�)perl 5.004�ȏ��K�v�Ƃ��܂��B
$ver = '2.1.2';  # �{�v���O�����̔Ő��B�֕ύX�B
;#+------------------------------------------------------------------------
;#|efCount[efStat�J�E���^��]
;#|(C)1998-2000 �s�v�c�G�̋�(http://yugen.main.jp/)
;#+------------------------------------------------------------------------
;# ������ ���ʂ̐ݒ荀��(�K�v) ������
;#+------------------------------------------------------------------------
;# [���샂�[�h]
;# SSI�Ƃ��ē��삳����Ȃ� 1 �C CGI�Ƃ��ē��삳����Ȃ� 0 �B
$USER{'SSIMode'} = 0;

;# [���O�t�@�C�����i�[�����f�B���N�g���̖��O]
;# ���O�p�f�B���N�g���� fstat/ �ȉ��ɍ���ĉ������B
$USER{'DIR_Log'} = 'log';

;# [�A�N�Z�X���O�ő�ۑ���]
;# 1�ȏ�A3000�����̐��l����͂��ĉ������B
$USER{'MaxLog'} = 1000;

;# [�ēǂݍ��ݖh�~�@�\(IP�`�F�b�N)�𗘗p���邩]
;# 1 = ����(�f�t�H���g) / 0 = ���Ȃ�(�d���J�E���g������)
$USER{'IPCheck'} = 1;

    ;# (IPCheck���P�̏ꍇ�L��)
    ;# [�ēǂݍ��ݖh�~�@�\�̗L������] (���P�ʂŎw��)
    ;# �w�肵�����Ԃ��o�ƁA����IP�ł����Ă��J�E���g���܂��B
    ;# 0���w�肷��ƁA����IP�̊Ԃ͂����ƃJ�E���g���܂���B
    $USER{'IPExpire'} = 0;

# [�J�E���g�A�b�v�����Ȃ��z�X�g���EIP�A�h���X]
# �����w��ł��܂����A���S��v���Ȃ���΂Ȃ�܂���B
# �������󗓂ɂ��Ă͂����܂���B�@�K���ŗǂ��ł����疄�߂ĉ������B
@USER_DenyIP = (
	'165.93.96.101',
	'abc123.ppp.test.ne.jp',
);

# [�J�E���g�A�b�v�����Ȃ��u���E�U]
# �����w��ł��܂��B�@�O����r���s���܂��B
# �������󗓂ɂ��Ă͂����܂���B�@�K���ŗǂ��ł����疄�߂ĉ������B
@USER_DenyAgent = (
	'WWWC',
	'Kerberos',
	'Monazilla',
);


;#+------------------------------------------------------------------------
;# ������ CGI�Ƃ��Ďg���Ƃ��̐ݒ荀�� ������
;#+------------------------------------------------------------------------
;# [�J�E���^�p�摜���i�[�����f�B���N�g���̖��O]
;# �J�E���^�摜�p�f�B���N�g���� fstat/ �ȉ��ɍ���ĉ������B
$USER{'Dir_Img'} = 'image';

	;# [�J�E���^�̃C���[�W�̖��O(�f�t�H���g�Ŏg�p���镨)]
	$USER{'DigitName'} = 'fuksan';


;#+------------------------------------------------------------------------
;# ������ SSI �Ƃ��Ďg���Ƃ��̐ݒ荀�� ������
;#+------------------------------------------------------------------------
;# [efStat�ꎮ���i�[�����f�B���N�g��]
;# ���Ăяo��HTML���猩�����΃p�X�ł��ǂ����A���[�g����̃t���p�X���]�܂����B
;# ���Ō�̃X���b�V��(/)�͕K���K�v�B
$USER{'SSI_Pass'} = '/home/sites/home/users/fuka/web/cgi-bin/fstat/';


;#+------------------------------------------------------------------------
;# ������ ���̑��A�⏕�I�ȍ��� ������
;#+------------------------------------------------------------------------
# [gifcat.pl�̂��肩 (�ʏ�͕ύX���Ȃ��ŉ�����)]
$USER{'GifCat'} = './lib/gifcat.pl';


#+------------------------------------------------------------------------
# (�ݒ肱���܂�)
#+------------------------------------------------------------------------
# ����������͕�����l�����M���ĉ������B
# �@(�^�u�̃T�C�Y�E[4]�A�ܕԂ��E[����]���Y��ɕ\������܂�)
#+------------------------------------------------------------------------
#|&main
#+------------------------------------------------------------------------
&Macro_Setup;				# �e�평����
&Macro_Access;				# �A�N�Z�X�L�^
&Macro_LoadData;			# ���O�t�@�C����ǂݍ���
&Macro_Check;				# �`�F�b�N
if ($OutputOnly) {			# �d���A�N�Z�X�͋L�^���Ȃ�
	&Macro_Output;			# ���ʂ��o��
} else {
	&Macro_Count;			# �J�E���g
	&Macro_SaveData;		# �ۑ�
	&Macro_Output;			# ���ʂ��o��
}
exit;


#+------------------------------------------------------------------------
#|�v���O�����̗���Ƃ��ẴT�u���[�`��
#+------------------------------------------------------------------------
### �e�평����
sub Macro_Setup {
	$ENV{'TZ'} = 'JST-9';													# ���ϐ�TZ����{���Ԃɐݒ�
	$Digit = 0;
	$OutputOnly = 0;														# 1=�o�͂̂�

	### ���ݎ����̎擾
	$RUN_TIME   = time;														# ���ݎ���(�b�`��)
	@RUN_TIME   = localtime($RUN_TIME);										# ���ݎ���(�ϊ���)
	$RUN_TIME_E = &C62_Encode($RUN_TIME);									# �G���R�[�h�ό��ݎ���
	$RUN_week   = &TotalWeek($RUN_TIME[7]);									# ���ݏT

	### �����̉���
	foreach $data (split(/&/, $ENV{'QUERY_STRING'})) {
		($key , $val) = split(/=/,$data);
		$P{$key} = $val;
	}
	$Filename = $P{'LOG'};													# ���O�t�@�C����

	## SSI���[�h
	if ($USER{'SSIMode'}) {
		$USER{'DIR_Log'} = "${USER{'SSI_Pass'}}${USER{'DIR_Log'}}/";		# ���O�i�[�f�B���N�g��

		# ���샂�[�h
		if    ($P{'MODE'} eq '-') { $OutputOnly = 1; } 						# "-"�Ȃ�J�E���g����
		elsif ($P{'MODE'} eq 'h') { $OutMode = 'h' ; }						# "h"�Ȃ�o�͖���
	}

	## CGI���[�h
	else {
		# ���샂�[�h
		if ($P{'MODE'} =~ /^-([atyw])$/) {									# ���� - ������Ώo�͂̂�
			$OutMode = $1;
			$OutputOnly = 1;
		} elsif ($P{'MODE'} =~ /^([atyw])$/) {								# ������Ε��ʂɃ`�F�b�N
			$OutMode = $1;
		} else { $OutMode = 'a'; }											# �������Ȃ���΋����I�� a ��

		if ($P{'DIGIT'} > 20) { &Macro_PutError('e0001'); }					# ����
		else                  { $Digit = $P{'DIGIT'}-1; }

		$ENV{'HTTP_REFERER'} = $P{'REF'};									# �Q�ƌ�

		$screen = $P{'SCR'};												# ��ʏ��

		$USER{'DigitName'} = $P{'FONT'} if ($P{'FONT'} ne '');				# �t�H���g��

		## �f�B���N�g�������C��
		$USER{'DIR_Log'} = "./${USER{'DIR_Log'}}/";							# ���O�i�[�f�B���N�g��
		$USER{'Dir_Img'} = "./${USER{'Dir_Img'}}/${USER{'DigitName'}}/";	# �t�H���g�i�[�f�B���N�g��

		### �����\�����[�h�������炱���ŏI���
		if ($OutMode eq 'w') {
			$Digit = 0;
			print &Func_PutGIF(sprintf("%02dc%02d", $RUN_TIME[2], $RUN_TIME[1]));
			exit(0);
		}
	}
}


### [�A�N�Z�X�L�^]
sub Macro_Access {
	### �K��҂̃����[�g�z�X�g�擾
	$host = $ENV{'REMOTE_ADDR'};

	if ($host eq '') {
		$host = '-';
	} else {
		# proxy�`�F�b�N
		$host = $1 if ($ENV{'HTTP_FORWARDED'} =~ / for (.*)/);		# HTTP_FORWARDED (DeleGate , Squid)

		# IP -> HOST
		$host = gethostbyaddr(pack("C4", split(/\./, $host)), 2) || $host;
	}

	### ���[�U�G�[�W�F���g�擾
	$agent = $ENV{'HTTP_USER_AGENT'};
	$agent = 'Monazilla/1.0' if ($agent =~ /Seven\//);
	$agent =~ s'^Mozilla/'!';
	$agent =~ s"\(compatible; MSIE (.+)\)"(!$1)";
	$agent = '-' if ($agent eq '');								#�G�[�W�F���g�����Ȃ����'-'�ɒu��������

	### �Q�ƌ��擾
	$ref = $ENV{'HTTP_REFERER'};
	$ref =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack("C",hex($1))/ge;	# URLDecode
	$ref =~ s/\?$//;
	$ref =~ s"(/index\.)html$|\1htm$|\1shtml$|\1php3$"/"i;
	$ref =~ s'^http://'!'i;
	if (($ref eq '') || ($ref eq '[unknown origin]') ||			# �����N������, '[unknown origin]', 'bookmark'�Ȃ�'-'�ɒu��������
	    ($ref eq 'bookmarks') || ($ref eq "',ref,'"))
	{ $ref = '-'; }

	### ��ʃ��[�h
	if (($screen eq '') || ($screen !~ /^[0-9]/)) {
		$screen = '-';
	} else {
		($screen_x, $screen_y, $screen_color) = split(/,/, $screen);
		$screen_x		= &C62_Encode($screen_x);
		$screen_y		= &C62_Encode($screen_y);
		$screen_color	= &C62_Encode($screen_color);
		$screen = "$screen_x,$screen_y,$screen_color";
	}
}


### [���O�t�@�C����ǂݍ���]
sub Macro_LoadData {
	unless (open(LOG,"+<${USER{'DIR_Log'}}${Filename}.log")) {
		&Macro_PutError('e0000');
	}
	flock(LOG,2);
	for ($i=0 ; $i<8 ; $i++) { chomp($count[$i] = <LOG>); }		# �e��J�E���g��
	chomp(@log = <LOG>);										# �A�N�Z�X���O

	###�V�K���O�Ȃ�t�H�[�}�b�g
	if ($count[0] eq '') {
		$count[0] = "FC2\t${RUN_TIME_E}";
		$count[1] = "${RUN_TIME_E}\t0";
		$count[2] = "0\t0\t0\t0\t0\t0\t0\t0";
		$count[3] = "0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0";
		$count[4] = "0\t0\t0\t0\t0\t0\t0";
		$count[5] = "0\t0\t0\t0\t0\t0";
		$count[6] = "0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0";
		$count[7] = "0\t0\t0\t0\t0\t0";
	}

	# ���`���̃��O�Ȃ�ϊ�
	elsif ($count[0] !~ /^FC2/) {
		&Macro_Convert;
	}

	###�f�[�^���e�z��Ɋi�[
	($LOG_ID, $LOG_SINCE_E)			= split(/\t/, $count[0]);		#�w�b�_
	$LOG_SINCE						= &C62_Decode($LOG_SINCE_E);
	&Macro_PutError('e1110') if ($LOG_ID ne 'FC2');					# ���O�`��check(�@�\���Ȃ�?)

	($LOG_TIME_E, $ALL_E, $LOG_IP)	= split(/\t/, $count[1]);		# �e����
	$LOG_TIME						= &C62_Decode($LOG_TIME_E);
	$ALL							= &C62_Decode($ALL_E);

	@DAILY							= &split($count[2]);			# ���ʏW�v
	@HOUR							= &split($count[3]);			# ���ԕʏW�v
	@YOUBI							= &split($count[4]);			# �j���ʏW�v
	@WEEK							= &split($count[5]);			# �T�ʏW�v
	@MONTH							= &split($count[6]);			# ���ʏW�v
	@YEAR							= &split($count[7]);			# ���ʏW�v

	# ���O�̓��t�����߂�
	@LOG_TIME = localtime($LOG_TIME);
	$LOG_week = &TotalWeek($LOG_TIME[7]);

	# �������؂蕪���A10�i���ɖ߂�
	sub split {
		my($str) = @_;
		my(@array);

		@array = split(/\t/, $str);
		foreach (@array) { $_ = &C62_Decode($_); }
		return @array;
	}
}


### �J�E���g���ׂ��K��҂��`�F�b�N
sub Macro_Check {
	if ($USER{'IPCheck'}) {												# �d���J�E���g���������H
		if ($host eq $LOG_IP) {											# �O��K��҂Ɠ������H
			if ($USER{'IPExpire'} == 0) {
				$OutputOnly = 1;
			} else {
				if ($RUN_TIME - $LOG_TIME < $USER{'IPExpire'} * 60) {	# IP�͗L�������O���H
					$OutputOnly = 1;
				} else { $OutputOnly = 0; }
			}
		} else { $OutputOnly = 0; }
	} else { $OutputOnly = 0; }

	foreach (@USER_DenyIP) {											# �e���ׂ�IP���H
		if ($host eq $_) {
			$OutputOnly = 1;
			last;
		}
	}

	foreach (@USER_DenyAgent) {											# �e���ׂ��u���E�U���H
		if ($agent =~ /^$_/) {
			$OutputOnly = 1;
			last;
		}
	}
}


### [�J�E���g����]
sub Macro_Count {
	my($n);

	### �����Ԍo�߂��������߂�
	$n  = $RUN_TIME[7] - $LOG_TIME[7];
	$n += 366 if ($n < 0);			# �N���������ꍇ�␳(n+366���o��)

	if ($n == 0) { $DAILY[0]++; }	# ������
	elsif ($n > 0) {				# n���o��
		for (1 .. $n) { unshift(@DAILY, 0); }
		$DAILY[0] = 1;
	}

	### ���T�Ԍo�߂��������߂�
	$n  = $RUN_week - $LOG_week;
	$n += 53 if ($n < 0);			# �N���������ꍇ�␳(n+53�T�Ԍo��)

	if ($n == 0) { $WEEK[0]++; }	# �����T
	elsif ($n > 0) {				# n�T�Ԍo��
		for (1 .. $n) { unshift(@WEEK, 0); }
		$WEEK[0] = 1;
	}


	### ���N�Ԍo�߂��������߂�
	$n = $RUN_TIME[5] - $LOG_TIME[5];

	if (($n == 0) || ($n < 0)) { $YEAR[0]++; }	# �����N(�T�[�o�����v���Â��ꍇ�����̏���)
	elsif ($n > 0) {							# n�N�o��
		@MONTH = (0) x 12;						# ���ʏW�v��reset
		for (1 .. $n) { unshift(@YEAR, 0); }
		$YEAR[0] = 1;
	}

	++$ALL;
	++$HOUR [ ${RUN_TIME[2]} ];
	++$YOUBI[ ${RUN_TIME[6]} ];
	++$MONTH[ ${RUN_TIME[4]} ];
}


### [�J�E���g���ʂ�z��Ɋi�[]
sub Macro_SaveData {
	$ALL_E = &C62_Encode($ALL);

	$count[0] = "FC2\t$LOG_SINCE_E";									# �e����
	$count[1] = "$RUN_TIME_E\t$ALL_E\t$host";							# �e����
	$count[2] = &Func_Array2Str(8,  \@DAILY);							# ���ʏW�v
	$count[3] = &Func_Array2Str(24, \@HOUR);							# ���ԕʏW�v
	$count[4] = &Func_Array2Str(7,  \@YOUBI);							# �j���ʏW�v
	$count[5] = &Func_Array2Str(6,  \@WEEK);							# �T�ʏW�v
	$count[6] = &Func_Array2Str(12, \@MONTH);							# ���ʏW�v
	$count[7] = &Func_Array2Str(6,  \@YEAR);							# ���ʏW�v
	$new_log  = "$ALL_E\t$RUN_TIME_E\t$host\t$agent\t$ref\t$screen";	#�V�K���O�s

	unshift(@log, $new_log);											# �V�������O��t�������A
	splice(@log, $USER{'MaxLog'});										# �Â����O�͏�������

	seek(LOG,0,0);

	foreach (@count) { print LOG "$_\n"; }
	foreach (@log)   { print LOG "$_\n"; }

	truncate(LOG,tell);

	flock(LOG,8);
	close(LOG);

	### �z��̓��e����s�̕�����ɒ����֐�
	### $limit���傫�ȃf�[�^�͐؂�̂Ă�
	sub Func_Array2Str {
		my($limit, $array) = @_;
		splice(@$array, $limit);

		foreach (@$array) { $_ = &C62_Encode($_); }
		return join("\t", @$array);
	}
}


### [�J�E���g���o��]
sub Macro_Output {
	my($s, $m, $h, $d, $mo, $y, $w) = @RUN_TIME;
	my($today, $yesterday) = @DAILY;
	my($all) = $ALL;
	my(@w);

	unless ($OutputOnly) {
		$today      = &C62_Decode($today);
		$yesterday  = &C62_Decode($yesterday);
	}

	### SSI���[�h�Ȃ�
	if ($USER{'SSIMode'}) {
		print "Content-type: text/plain\n\n";
		if ($OutMode ne 'h') {
			$agent =~ s'^!'Mozilla/';
			$agent =~ s"\(!(.+)\)"(compatible; MSIE $1)";
			$ref   =~ s'^!'http://';
			++$mo;
			$y += 1900;

			;#+--[ * ���b�Z�[�W(���[�U�ύX��) * ]------------[ �������� ]-+

			# �D���ȗj���̕\�L��I��ŉ������B
			@w = ('��', '��','��','��','��','��','�y');  $w = $w[$w];
			# @w = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');  $w = $w[$w];

			;#+-----------------------------------------------------------+
			;#(���b�Z�[�W���̕ϐ��̈Ӗ�)
			;#  ${all}      �c���q�b�g��    ${y} �c�N    ${h}�c��
			;#  ${today}    �c�{���q�b�g��  ${mo}�c��    ${m}�c��
			;#  ${yesterday}�c����q�b�g��  ${d} �c��    ${s}�c�b
			;#  ${host}     �c�K��҃z�X�g  ${w} �c�j��
			;#  ${agent}    �c�u���E�U��
			;#  ${ref}      �c�Q�ƌ�        �� " �� \" �ɒu�������܂��傤�I
			;#+-----------------------------------------------------------+

			@mes = (
				#"${all}\n${today}\n${yesterday}\n${host}\n${agent}\n${ref}\n${y}�N${mo}��${d}��(${w})\n${h}��${m}��${s}�b\n",
				"<FONT FACE=\"Arial\">Total:<B>${all}</B> / Today:<B>${today}</B> / Yesterday:<B>${yesterday}</B></FONT>",
				#"<FONT SIZE=+1><B>�҂��`�����`��</B></FONT>�@�S����<B>${all}���{���g</B>�E������<B>${today}���{���g</B>�E�����<B>${yesterday}���{���g</B>�̒~�d",
				#"�͒����I�@�O���ɋ@�e�m�F�I���莯�ʔԍ�<B>${host}</B>���I<BR>�G�@�ł��I �R���f�B�V�����E���b�h�b�b�b�I�I<BR>���̐��A�O����<B>${all}�@</B>�b�I�@������<B>${today}�@</B>�I�@�E����<B>${yesterday}�@</B>�I�@�g���C�p�ӂ��܂���!?(��)",
			);

			;#+--[ * ���b�Z�[�W(���[�U�ύX��) * ]------------[ �����܂� ]-+

			# �����_���ɑI��
			srand(time + $$);
			$n = int(rand($#mes+1));

			# �\��
			print $mes[$n];
		}
	}

	### CGI���[�h�Ȃ�
	else {
		# ���A�N�Z�X��
		if    ($OutMode eq 'a') { print &Func_PutGIF($all); }
		# �����A�N�Z�X��
		elsif ($OutMode eq 't') { print &Func_PutGIF($today); }
		# ����A�N�Z�X��
		elsif ($OutMode eq 'y') { print &Func_PutGIF($yesterday); }
	}
}


### [gif���o��]
sub Func_PutGIF {
	my($Data) = @_;
	my($i, $n, @array);

	require $USER{'GifCat'};
	print "Content-type: image/gif\n";
	print "Expires: 01/01/1970 00:00:00 JST\n\n";	# �L���b�V���𖳌��ɂ���
	binmode(STDOUT);

	### �������w�肳�ꂽ��A����Ȃ�����0�ŕ₤
	$Data = ('0'x($Digit-(length($Data)-1))).$Data if (length($Data)-1 < $Digit);

	for ($i=0 ; $i < length($Data) ; $i++) {
		$n = substr($Data, $i, 1);
		push(@array, "${USER{'Dir_Img'}}${n}${USER{'DigitName'}}.gif");
	}

	return &gifcat'gifcat(@array);
}


### [�G���[�o��]
# e0000 = �t�@�C���I�[�v�����s
# e0001 = �������ӂ�
# e1110 = ���O�̌`�����s��
# e1111 = �����ȃI�v�V����
sub Macro_PutError {
	my($code) = @_;

	if ($USER{'SSIMode'}) {
		print "Content-type: text/plain\n\n";
		if ($code eq 'e0000') {
			print "<P><B>[efCount $ver(SSI)]���O���J�����Ƃ��o���܂���ł���</B><br>${USER{'DIR_Log'}}${Filename}.log</P>\n";
		} elsif ($code eq 'e1110') {
			print "<P><B>[efCount $ver(SSI)]���O�̌`�����s���ł�</B></P>\n";
		} elsif ($code eq 'e1111') {
			print "<P><B>[efCount $ver(SSI)]�����ȃI�v�V�����ł�</B></P>\n";
		} else {
			print "<P><B>[efCount $ver(SSI)]����`�̃G���[�ł�</B></P>\n";
		}
	} else {
		require $USER{'GifCat'};
		print "Content-type: image/gif\n\n";
		binmode(STDOUT);
		for ($i=0 ; $i < length($code) ; $i++) {
			$n = substr($code, $i, 1);
			push(@Digit, "./lib/${n}.gif");
		}
		print &gifcat'gifcat(@Digit);
	}
	exit(1);
}


sub Macro_Convert {
	my($num, $time, $host, $agent, $ref, $screen,
	   $day, $week, $time, $all,   $ip,  $i,      @work);

	for ($i = 1; $i < 6; $i++) {
		split(/#/, $count[$i]);
		foreach (@_) { $_ = &C62_Encode($_); }
		$count[$i] = join("\t", @_);
	}

	($day, $week, $time, $all, $ip) = split(/#/, $count[0]);

	$all_e = &C62_Encode($all);

	# �J�E���g�L�^���̕ϊ�
	# ��U��Ɨp�z��ɓ����
	$work[0] = "FC2\t${RUN_TIME_E}";
	$work[1] = "${RUN_TIME_E}\t${all_e}\t${ip}";
	$work[2] = $count[1];
	$work[3] = $count[2];
	$work[4] = $count[3];
	$work[5] = $count[4];
	$work[6] = $count[5];
	$work[7] = "0\t0\t0\t0\t0\t0";
	unshift(@log,$count[6]);	# ���ēǂݍ��܂ꂽ�A�N�Z�X���O
	@count = @work;				# �����z��

	# ���O�L�^���̕ϊ�
	foreach (@log) {
		($num, $time, $host, $agent, $ref, $screen) = split(/#/, $_);
		$num   = &C62_Encode($num);
		$time  = &C62_Encode($time);
		$agent =~ s/%23/#/g;
		$agent =~ s'^Mozilla/'!';
		$agent =~ s"\(compatible; MSIE (.+)\)"(!$1)";
		$ref   =~ s'^http://'!'i;
		$_     = "$num\t$time\t$host\t$agent\t$ref\t$screen";
	}
}


### �ʎZ�T�����߂�֐�
sub TotalWeek {
	my($total) = @_;
	my($week);

	if ($total < 7) { $week = 0; }				# 0���Z�΍�
	else            { $week = int($total/7); }

	return $week;
}


;### 62�i����10�i��
sub C62_Decode {
	my $str = reverse($_[0]);
	my($digit, $i);

	for ($i = 0; $i < length($str); $i++) {
		$digit += index('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', substr($str, $i, 1)) * (62 ** $i);
	}

	return $digit;
}


;### 10�i����62�i��
sub C62_Encode {
	my($digit) = $_[0];
	my($str);

	if (!$digit) {
		return 0;
	} else {
		while ($digit) {
			$str .= substr('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', ($digit % 62), 1);
			$digit = int($digit / 62);
		}
		return reverse($str);
	}
}
