package MIME;
# Copyright (C) 1993-94,1997 Noboru Ikuta <noboru@ikuta.ichihara.chiba.jp>
#
# mimew.pl: MIME encoder library Ver.2.02 (1997/12/30)

$main'mimew_version = "2.02";

# �C���X�g�[�� : @INC �̃f�B���N�g���i�ʏ�� /usr/local/lib/perl�j�ɃR�s�[
#                ���ĉ������B
#
# �g�p��1 : require 'mimew.pl';
#           $from = "From: ���c �� <noboru\@ikuta.ichihara.chiba.jp>";
#           print &mimeencode($from);
#
# �g�p��2 : # UNIX��Base64�G���R�[�h����ꍇ
#           require 'mimew.pl';
#           undef $/;
#           $body = <>;
#           print &bodyencode($body);
#           print &benflush;
#
# &bodyencode($data,$coding):
#   �f�[�^��Base64�`���܂���Quoted-Printable�`���ŃG���R�[�h����B
#   ��2�p�����[�^��"qp"�܂���"b64"���w�肷�邱�Ƃɂ��R�[�f�B���O�`��
#   ���w�����邱�Ƃ��ł���B��2�p�����[�^���ȗ������Base64�`���ŃG��
#   �R�[�h����B
#   Base64�`���̃G���R�[�h�̏ꍇ�́A$foldcol*3/4 �o�C�g�P�ʂŕϊ�����
#   �̂ŁA�n���ꂽ�f�[�^�̂������[�ȕ����̓o�b�t�@�ɕۑ����ꎟ�ɌĂ΂�
#   ���Ƃ��ɏ��������B�Ō�Ƀo�b�t�@�Ɏc�����f�[�^��&benflush���Ă�
#   ���Ƃɂ�菈������o�b�t�@����N���A�����B
#   Quoted-Printable�`���̃G���R�[�h�̏ꍇ�́A�s�P�ʂŕϊ����邽�߁A
#   �f�[�^�̍Ō�ɉ��s�����������ꍇ�A�Ō�̉��s�����̌��̃f�[�^��
#   �o�b�t�@�ɕۑ�����A���ɌĂ΂ꂽ�Ƃ��ɏ��������B�Ō�Ƀo�b�t�@
#   �Ɏc�����f�[�^��&benflush("qp")���ĂԂ��Ƃɂ�菈������o�b�t�@
#   ����N���A�����B
#
# &benflush($coding):
#   ��1�p�����[�^��"b64"�܂���"qp"���w�肷�邱�Ƃɂ��A���ꂼ��Base64
#   �`���܂���Quoted-Printable�`���̃G���R�[�h���w�肷�邱�Ƃ��ł���B
#   ��1�p�����[�^�ɉ����w�肵�Ȃ����Base64�`���ŃG���R�[�h�����B
#   Base64�̃G���R�[�h�̏ꍇ�A&bodyencode���������c�����f�[�^��������
#   pad�������o�͂���BQuoted-Printable�̏ꍇ�A�s�P�ʂłȂ��u���b�N�P
#   �ʂ�&bodyencode���Ăԏꍇ�A&bodyencode���������c�����f�[�^������
#   �o�b�t�@�Ɏc���Ă���΂������������B
#   ��̃f�[�^��(1��܂��͉��񂩂ɕ�����)&bodyencode������ɕK��1��
#   �ĂԕK�v������B
#
# &mimeencode($text):
#   ��1�p�����[�^�����{�ꕶ������܂�ł���΁A���̕�����ISO-2022-JP��
#   �ϊ��������ƁAMIME encoded-word(RFC2047�Q��)�ɕϊ�����B�K�v�ɉ���
#   ��encoded-word�̕�����encoded-word�̑O��ł̍s�������s���B
#
#   �����R�[�h�̎�������́A����s��ShiftJIS��EUC�����݂��Ă���ꍇ��
#   �����Ċ����R�[�h�̍��݂ɂ��Ή����Ă���BShiftJIS��EUC���ǂ����Ă�
#   ���f�ł��Ȃ��Ƃ���$often_use_kanji�ɐݒ肳��Ă���R�[�h�Ɣ��肷��B
#   ISO-2022-JP�̃G�X�P�[�v�V�[�P���X��$jis_in��$jis_out�ɐݒ肷�邱��
#   �ɂ��ύX�\�ł���B

$often_use_kanji = 'SJIS'; # or 'EUC'

$jis_in  = "\x1b\$B"; # ESC-$-B ( or ESC-$-@ )
$jis_out = "\x1b\(B"; # ESC-(-B ( or ESC-(-J )

# �z�z���� : ���쌠�͕������܂��񂪁A�z�z�E���ς͎��R�Ƃ��܂��B���ς���
#            �z�z����ꍇ�́A�I���W�i���ƈقȂ邱�Ƃ𖾋L���A�I���W�i��
#            �̃o�[�W�����i���o�[�ɉ��ϔŃo�[�W�����i���o�[��t�������`
#            �Ⴆ�� Ver.2.02-XXXXX �̂悤�ȃo�[�W�����i���o�[��t���ĉ�
#            �����B�Ȃ��ACopyright�\���͕ύX���Ȃ��ł��������B
#
# ���� : &mimeencode��jperl1.X(��2�o�C�g�����Ή����[�h)�Ŏg�p����ƁASJIS
#        ��EUC�����܂�7bit JIS(ISO-2022-JP)�ɕϊ��ł��܂���B
#        ���͂Ɋ܂܂�镶����7bit JIS(ISO-2022-JP)��ASCII�݂̂ł��邱��
#        ���ۏ؂���Ă���ꍇ�������A�K��original�̉p��ł�perl�i�܂���
#        jperl1.4�ȏ�� -Llatin �I�v�V�����t���j�œ������Ă��������B
#        �Ȃ��APerl5�Ή���jperl�͎��������Ƃ��Ȃ��̂łǂ̂悤�ȓ���ɂȂ�
#        ���킩��܂���B
#
# �Q�� : RFC1468, RFC2045, RFC2047

## MIME base64 �A���t�@�x�b�g�e�[�u���iRFC2045���j
%mime = (
"000000", "A",  "000001", "B",  "000010", "C",  "000011", "D",
"000100", "E",  "000101", "F",  "000110", "G",  "000111", "H",
"001000", "I",  "001001", "J",  "001010", "K",  "001011", "L",
"001100", "M",  "001101", "N",  "001110", "O",  "001111", "P",
"010000", "Q",  "010001", "R",  "010010", "S",  "010011", "T",
"010100", "U",  "010101", "V",  "010110", "W",  "010111", "X",
"011000", "Y",  "011001", "Z",  "011010", "a",  "011011", "b",
"011100", "c",  "011101", "d",  "011110", "e",  "011111", "f",
"100000", "g",  "100001", "h",  "100010", "i",  "100011", "j",
"100100", "k",  "100101", "l",  "100110", "m",  "100111", "n",
"101000", "o",  "101001", "p",  "101010", "q",  "101011", "r",
"101100", "s",  "101101", "t",  "101110", "u",  "101111", "v",
"110000", "w",  "110001", "x",  "110010", "y",  "110011", "z",
"110100", "0",  "110101", "1",  "110110", "2",  "110111", "3",
"111000", "4",  "111001", "5",  "111010", "6",  "111011", "7",
"111100", "8",  "111101", "9",  "111110", "+",  "111111", "/",
);

## JIS�R�[�h(byte��)��encoded-word �̕������Ή�
%mimelen = (
 8,30, 10,34, 12,34, 14,38, 16,42,
18,42, 20,46, 22,50, 24,50, 26,54,
28,58, 30,58, 32,62, 34,66, 36,66,
38,70, 40,74, 42,74,
);

## �w�b�_�G���R�[�h���̍s�̒����̐���
$limit=74; ## �����Ӂ� $limit��75���傫�������ɐݒ肵�Ă͂����Ȃ��B

## �{�f�Bbase64�G���R�[�h���̍s�̒����̐���
$foldcol=72; ## �����Ӂ� $foldcol��76�ȉ���4�̔{���ɐݒ肷�邱�ƁB

## �{�f�BQuoted-Printable�G���R�[�h���̍s�̒����̐���
$qfoldcol=75; ## �����Ӂ� $foldcol��76�ȉ��ɐݒ肷�邱�ƁB

## null bit�̑}���� pad�����̑}���̂��߂̃e�[�u��
@zero = ( "", "00000", "0000", "000", "00", "0" );
@pad  = ( "", "===",   "==",   "=" );

## ASCII, 7bit JIS, Shift-JIS �y�� EUC �̊e�X�Ƀ}�b�`����p�^�[��
$match_ascii = '\x1b\([BHJ]([\t\x20-\x7e]*)';
$match_jis = '\x1b\$[@B](([\x21-\x7e]{2})*)';
$match_sjis = '([\x81-\x9f\xe0-\xfc][\x40-\x7e\x80-\xfc])+';
$match_euc  = '([\xa1-\xfe]{2})+';

## MIME Part 2(charset=`ISO-2022-JP',encoding=`B') �� head �� tail
$mime_head = '=?ISO-2022-JP?B?';
$mime_tail = '?=';

## &bodyencode ���g�������c���f�[�^�p�o�b�t�@
$benbuf = "";

## &bodyencode �̏����P�ʁi�o�C�g�j
$bensize = int($foldcol/4)*3;

## &mimeencode interface ##
sub main'mimeencode {
    local($_) = @_;
    s/$match_jis/$jis_in$1/go;
    s/$match_ascii/$jis_out$1/go;
    $kanji = &checkkanji;
    s/$match_sjis/&s2j($&)/geo if ($kanji eq 'SJIS');
    s/$match_euc/&e2j($&)/geo if ($kanji eq 'EUC');
    s/(\x1b[\$\(][BHJ@])+/$1/g;
    1 while s/(\x1b\$[B@][\x21-\x7e]+)\x1b\$[B@]/$1/;
    1 while s/$match_jis/&mimeencode($&,$`,$')/eo;
    s/$match_ascii/$1/go;
    $_;
}

## &bodyencode interface ##
sub main'bodyencode {
    local($_,$coding) = @_;
    if (!defined($coding) || $coding eq "" || $coding eq "b64"){
	$_ = $benbuf . $_;
	local($cut) = int((length)/$bensize)*$bensize;
	$benbuf = substr($_, $cut+$[);
	$_ = substr($_, $[, $cut);
	$_ = &base64encode($_);
	s/.{$foldcol}/$&\n/g;
    }elsif ($coding eq "qp"){
	# $benbuf ����łȂ���΃f�[�^�̍ŏ��ɒǉ�����
	$_ = $benbuf . $_;

	# ���s�����𐳋K������
	s/\r\n/\n/g;
	s/\r/\n/g;

	# �f�[�^���s�P�ʂɕ�������(�Ō�̉��s�����ȍ~�� $benbuf �ɕۑ�����)
	@line = split(/\n/,$_,-1);
	$benbuf = pop(@line);

	local($result) = "";
	foreach (@line){
	    $_ = &qpencode($_);
	    $result .= $_ . "\n";
	}
	$_ = $result;
    }
    $_;
}

## &benflush interface ##
sub main'benflush {
    local($coding) = @_;
    local($ret) = "";
    if ((!defined($coding) || $coding eq "" || $coding eq "b64")
	&& $benbuf ne ""){
        $ret = &base64encode($benbuf) . "\n";
        $benbuf = "";
    }elsif ($coding eq "qp" && $benbuf ne ""){
	$ret = &qpencode($benbuf) . "\n";
	$benbuf = "";
    }
    $ret;
}

## MIME �w�b�_�G���R�[�f�B���O
sub mimeencode {
    local($_, $befor, $after) = @_;
    local($back, $forw, $blen, $len, $flen, $str);
    $befor = substr($befor, rindex($befor, "\n")+1);
    $after = substr($after, 0, index($after, "\n")-$[);
    $back = " " unless ($befor eq ""
                     || $befor =~ /[ \t\(]$/);
    $forw = " " unless ($after =~ /^\x1b\([BHJ]$/
                     || $after =~ /^\x1b\([BHJ][ \t\)]/);
    $blen = length($befor);
    $flen = length($forw)+length($&)-3 if ($after =~ /^$match_ascii/o);
    $len = length($_);
    return "" if ($len <= 3);
    if ($len > 39 || $blen + $mimelen{$len+3} > $limit){
        if ($limit-$blen < 30){
            $len = 0;
        }else{
            $len = int(($limit-$blen-26)/4)*2+3;
        }
        if ($len >= 5){
            $str = substr($_, 0, $len).$jis_out;
            $str = &base64encode($str);
            $str = $mime_head.$str.$mime_tail;
            $back.$str."\n ".$jis_in.substr($_, $len);
        }else{
            "\n ".$_;
        }
    }else{
        $_ .= $jis_out;
        $_ = &base64encode($_);
        $_ = $back.$mime_head.$_.$mime_tail;
        if ($blen + (length) + $flen > $limit){
            $_."\n ";
        }else{
            $_.$forw;
        }
    }
}

## MIME base64 �G���R�[�f�B���O
sub base64encode {
    local($_) = @_;
    $_ = unpack("B".((length)<<3), $_);
    $_ .= $zero[(length)%6];
    s/.{6}/$mime{$&}/go;
    $_.$pad[(length)%4];
}

## Quoted-Printable �G���R�[�f�B���O
sub qpencode {
    local($_) = @_;

    # `=' ������16�i�\���ɕϊ�����
    s/=/=3D/g;

    # �s���̃^�u�ƃX�y�[�X��16�i�\���ɕϊ�����
    s/\t$/=09/;
    s/ $/=20/;

    # �󎚉\����(`!'�``~')�ȊO�̕�����16�i�\���ɕϊ�����
    s/([^!-~ \t])/&qphex($1)/ge;

    # 1�s��$qfoldcol�����ȉ��ɂȂ�悤�Ƀ\�t�g���s�������
    local($folded, $line) = "";
    while (length($_) > $qfoldcol){
	$line = substr($_, 0, $qfoldcol-1);
	if ($line =~ /=$/){
	    $line = substr($_, 0, $qfoldcol-2);
	    $_ = substr($_, $qfoldcol-2);
	}elsif ($line =~ /=[0-9A-Fa-f]$/){
	    $line = substr($_, 0, $qfoldcol-3);
	    $_ = substr($_, $qfoldcol-3);
	}else{
	    $_ = substr($_, $qfoldcol-1);
	}
	$folded .= $line . "=\n";
    }
    $folded . $_;
}

sub qphex {
    local($_) = @_;
    $_ = '=' . unpack("H2", $_);
    tr/a-f/A-F/;
    $_;
}

## Shift-JIS �� EUC �̂ǂ���̊����R�[�h���܂܂�邩���`�F�b�N
sub checkkanji {
    local($sjis,$euc);
    $sjis += length($&) while(/$match_sjis/go);
    $euc  += length($&) while(/$match_euc/go);
    return 'NONE' if ($sjis == 0 && $euc == 0);
    return 'SJIS' if ($sjis > $euc);
    return 'EUC'  if ($sjis < $euc);
    $often_use_kanji;
}

## EUC �� 7bit JIS �ɕϊ�
sub e2j {
    local($_) = @_;
    tr/\xa1-\xfe/\x21-\x7e/;
    $jis_in.$_.$jis_out;
}

## Shift-JIS �� 7bit JIS �ɕϊ�
sub s2j {
    local($string);
    local(@ch) = split(//, $_[0]);
    while(($j1,$j2)=unpack("CC",shift(@ch).shift(@ch))){
        if ($j2 > 0x9e){
            $j1 = (($j1>0x9f ? $j1-0xb1 : $j1-0x71)<<1)+2;
            $j2 -= 0x7e;
        }
        else{
            $j1 = (($j1>0x9f ? $j1-0xb1 : $j1-0x71)<<1)+1;
            $j2 -= ($j2>0x7e ? 0x20 : 0x1f);
        }
        $string .= pack("CC", $j1, $j2);
    }
    $jis_in.$string.$jis_out;
}
1;
