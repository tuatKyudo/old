#!/usr/bin/perl

# RSS for YY-BOARD Ver1.0.2
# Copyright (c) 2004-2005 by CGI-Store.JP. All Rights Reserved.
# ��ʁF�t���[�E�F�A
# �J���ҁFCGI-Store.JP
# �A����Fwebmaster@cgi-store.jp
# �T�|�[�g�F�z�[���y�[�W�̌f���̂�
# �z�[���y�[�W�Fhttp://cgi-store.jp/

# ====================================================================
# ���ӎ���
# ====================================================================

# ����CGI���g�p���������Ȃ鑹�Q�ɑ΂��ĊJ���҂͈�؂̐ӔC�𕉂��܂���B
# RSS for YY-BOARD �Ɋւ��鎿��́ACGI-Store.JP �ɂ��肢���܂��B
# �T�|�[�g�̓z�[���y�[�W�̌f���݂̂Ŏ󂯕t���A
# ���ڃ��[���ɂ��T�|�[�g�͈�؍s���Ă��܂���B

# YY-BOARD v5.xx �̃��O�ɂ̂ݑΉ����Ă��܂��B
# YY-BOARD �̊e��h���o�[�W�����ł��A���O�`���������Ȃ�Ύg�p�\�ł��B

# YY-BOARD v5.4 �𓯍�������������܂��B

# ====================================================================
# �ݒu���@
# ====================================================================

# yyrss.cgi�̐ݒ�
# �ݒ荀�ڂ��ԈႢ�̖����悤�ɐݒ肵�Ă��������B
# yyrss.cgi�̃p�[�~�b�V������755���ɕύX�����s�\�ȏ�Ԃɂ��Ă��������B
# �Ō�ɁAyyrss.cgi�ւ̃����N���AYY-BOARD��z�[���y�[�W���ɑ}�����܂��B
# ������YY-BOARD�ɂ́Ayyrss.cgi�ւ̃����N��ݒu�ς݂ł��B

# ====================================================================
# �����R�[�h
# ====================================================================

# Perl�̃��W���[���ł���Jcode.pm�����p�s�\�����o����ƁA
# ������jcode.pl�𗘗p���悤�Ƃ��܂��B
# ���̏ꍇjcode.pl���p�X�����킹�Ă��������B

# ====================================================================
# ���ŗ���
# ====================================================================

# [Ver1.0.2] UTF-8�ɑΉ����܂����B
#            RSS�o�͂���\���Ώۂ̋L����2��ނ̕��@�Őݒ�\�ɂ����B
#            YY-BOARD�̐ݒ�t�@�C���uyyini.cgi�v�̓ǂݍ��݂��~�߂��B
# [Ver1.0.1] ��ʌ��J�B

# ====================================================================
# ���܂�
# ====================================================================

# �usample_icon�v�t�H���_�ɂ���A�C�R���́A
# �E�̓I�����C���̊Ǘ��҂̂����ӂɂ��A
# CGI-Store.Net ���ARSS for YY-BOARD �Ƌ��ɔz�z������̂ł��B

# �E�̓I�����C��
# http://park2.wakwak.com/~dol/

# ====================================================================
# �ݒ荀�ڂ�������
# ====================================================================

# Jcode.pm or jcode.pl
BEGIN {
	eval {
		require Jcode;
		$rss_UseJcodeModule = 1;
	};
	if ($@) {
		# Jcode.pm���g�p�ł��Ȃ�����jcode.pl���g�p���܂��B
		require './lib/jcode.pl';   # �����p���ɍ����悤�p�X���C�����Ă��������B
		$rss_UseJcodeModule = 0;
	}
}

# �o�͂��镶���R�[�h�i�K�{�j�uutf8�v��Jcode.pm���p���̂ݎg�p�\�ł��B
$rss_oe = 'sjis';    # sjis or euc or utf8

# ���̃t�@�C����URL�i�K�{�j
$rss_file = 'http://www.tuat.ac.jp/~kyudo/cgi-bin/yybbs/yyrss.cgi';

# �f���̊ȒP�Ȑ����i�K�{�j
$rss_setsumei = '�|�����f����';

# �\���Ώ�
#  1 -> ��ԐV�����X���b�h���̋L�����ő匏�������\������B
#  2 -> �X���b�h���ɃX���b�h�J�n�̋L�����ő匏�������\������B
$rss_type = 2;

# �o�͂���ő匏���i�K�{�j
$rss_num = 5;

# YY-BOARD�̃^�C�g���i�K�{�j
$title = 'BBS';

# YY-BOARD��URL�i�K�{�j�i��΃p�X�j
$script = 'http://www.tuat.ac.jp/~kyudo/cgi-bin/yybbs/yybbs.cgi';

# YY-BOARD�̃��O�t�@�C��
$logfile = './data/log.cgi';

# ====================================================================
# �ݒ荀�ڂ����܂�
# ====================================================================


# HTTP�w�b�_
if ($rss_UseJcodeModule == 1) {
	if ($rss_oe eq 'utf8') {
		print 'Content-Type: text/xml; charset="UTF-8"' . "\n";
	} elsif ($rss_oe eq 'euc') {
		print 'Content-Type: text/xml; charset="EUC-JP"' . "\n";
	} else {
		print 'Content-Type: text/xml; charset="Shift_JIS"' . "\n";
	}
} else {
	if ($rss_oe eq 'euc') {
		print 'Content-Type: text/xml; charset="EUC-JP"' . "\n";
	} else {
		print 'Content-Type: text/xml; charset="Shift_JIS"' . "\n";
	}
}
print 'Pragma: no-cache' . "\n";
print 'Cache-Control: no-cache' . "\n";
print "\n";

# XML�w�b�_
if ($rss_UseJcodeModule == 1) {
	if ($rss_oe eq 'utf8') {
		print '<?xml version="1.0" encoding="UTF-8" ?>' . "\n";
	} elsif ($rss_oe eq 'euc') {
		print '<?xml version="1.0" encoding="EUC-JP" ?>' . "\n";
	} else {
		print '<?xml version="1.0" encoding="Shift_JIS" ?>' . "\n";
	}
} else {
	if ($rss_oe eq 'euc') {
		print '<?xml version="1.0" encoding="EUC-JP" ?>' . "\n";
	} else {
		print '<?xml version="1.0" encoding="Shift_JIS" ?>' . "\n";
	}
}
print '<rdf:RDF' . "\n";
print '  xmlns="http://purl.org/rss/1.0/"' . "\n";
print '  xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"' . "\n";
print '  xmlns:dc="http://purl.org/dc/elements/1.1/"' . "\n";
print '  xml:lang="ja">' . "\n";

# �ݒ�l�̕����R�[�h��ϊ�
if ($rss_UseJcodeModule == 1) {
	if ($rss_oe eq 'utf8') {
		Jcode::convert(\$title, 'utf8', 'sjis');
		Jcode::convert(\$script, 'utf8', 'sjis');
		Jcode::convert(\$rss_file, 'utf8', 'sjis');
		Jcode::convert(\$rss_setsumei, 'utf8', 'sjis');
	} elsif ($rss_oe eq 'euc') {
		Jcode::convert(\$title, 'euc', 'sjis');
		Jcode::convert(\$script, 'euc', 'sjis');
		Jcode::convert(\$rss_file, 'euc', 'sjis');
		Jcode::convert(\$rss_setsumei, 'euc', 'sjis');
	}
}
else {
	if ($rss_oe eq 'euc') {
		&jcode::convert(\$title, 'euc', 'sjis');
		&jcode::convert(\$script, 'euc', 'sjis');
		&jcode::convert(\$rss_file, 'euc', 'sjis');
		&jcode::convert(\$rss_setsumei, 'euc', 'sjis');
	}
}

# �f�[�^���o
@viewdata = ();
open(LOGF, $logfile);
flock(LOGF, 2);
$temp = <LOGF>;
$Scheck = 0;
while ($temp = <LOGF>) {
	if ($rss_type == 1) {
		if ((split(/<>/, $temp))[1] eq '') { $Scheck++; }
		if ($Scheck >= 2) { last; }
	} else {
		if ((split(/<>/, $temp))[1] ne '') { next; }
	}
	if ($rss_UseJcodeModule == 1) {
		if ($rss_oe eq 'utf8') {
			Jcode::convert(\$temp, 'utf8', 'sjis');
		} elsif ($rss_oe eq 'euc') {
			Jcode::convert(\$temp, 'euc', 'sjis');
		}
	} else {
		if ($rss_oe eq 'euc') {
			&jcode::convert(\$temp, 'euc', 'sjis');
		}
	}
	push @viewdata, $temp;
}
close(LOGF);

if ($rss_type == 1) {
	@viewdata = reverse @viewdata;
}

if ($rss_num > $#viewdata + 1) { $rss_num = $#viewdata + 1; }

print ' <channel rdf:about="' . $rss_file . '">' . "\n";
print '  <title>' . $title . '</title>' . "\n";
print '  <link>' . $script . '</link>' . "\n";
print '  <description>' . $rss_setsumei . '</description>' . "\n";
print '  <items>' . "\n";
print '   <rdf:Seq>' . "\n";
for ($i = 1; $i <= $rss_num; $i++) {
	print '    <rdf:li rdf:resource="' . $script . '"/>' . "\n";
}
print '   </rdf:Seq>' . "\n";
print '  </items>' . "\n";
print ' </channel>' . "\n";

for ($i = 0; $i <= $#viewdata; $i++) {
	if ($i >= $rss_num) { last; }
	@values = split(/<>/, $viewdata[$i]);
	for ($j = 0; $j <= $#values; $j++) {
		if ($j == 2) {
			$values[$j] = substr($values[$j], 0, 4) . '-' . substr($values[$j], 5, 2) . '-' . substr($values[$j], 8, 2) . 'T' . substr($values[$j], -5, 2) . ':' . substr($values[$j], -2, 2) . '+09:00';
			
		}
		else {
			$values[$j] =~ s/<BR>/ /g;
			$values[$j] =~ s/<br>/ /g;
		}
	}
	print ' <item rdf:about="' . $script . '">' . "\n";
	print '  <title>' . $values[5] . '</title>' . "\n";
	print '  <link>' . $script . '</link>' . "\n";
	print '  <description>' . $values[6] . '</description>' . "\n";
	print '  <dc:date>' . $values[2] . '</dc:date>' . "\n";
	print '  <dc:creator>' . $values[3] . '</dc:creator>' . "\n";
	print ' </item>' . "\n";
}

print '</rdf:RDF>' . "\n";

exit;

