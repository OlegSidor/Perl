#!/usr/bin/perl
=head1
 Name FormSaver
 Version 1.0
 Description
        Save a form data to the file

=cut
use strict;
use warnings FATAL => 'all';
use Data::Dumper;

use CGI;
use CGI::Carp qw(fatalsToBrowser);
use Template;
use File::Basename;
use DBI;
use MIME::Base64 qw(encode_base64);

print "Content-Type: text/html\n\n";

my $q = CGI->new();

my $dbh = DBI->connect(
    "dbi:mysql:dbname=test",
    "OldNeer",
    "Oleg1122_l",
    { RaiseError => 1 },
) or die $DBI::errstr;

my @params = $q->param();
if (@params) {
    open(my $file, '>', 'data.txt');
    foreach my $p (@params) {
        my $value = $q->param($p);
        print $file "$p = $value\n";
    }
    close($file);
    my $img = $q->upload("img");
    my $name = $q->param("name");
    my $email = $q->param("email");
    my ($image, $buff);
    while (read $img, $buff, 1024) {
        $image .= $buff;
    }
    my $stm = $dbh->prepare("INSERT INTO Users(`name`, `email`, `img`) VALUES (?, ?, ?)");
    $stm->bind_param(1, $name, DBI::SQL_VARCHAR);
    $stm->bind_param(2, $email, DBI::SQL_VARCHAR);
    $stm->bind_param(3, $image, DBI::SQL_BLOB);
    $stm->execute();
    print "<script>location = location;</script>"
}

my $sth = $dbh->prepare("SELECT * FROM Users");
$sth->execute();
my $items = $sth->fetchall_hashref('id');

foreach (values %$items) {
    $_->{img} = encode_base64($_->{img});
}

my $config = {
    INCLUDE_PATH => '.',
    INTERPOLATE  => 1,
    POST_CHOMP   => 1,
    PRE_PROCESS  => '',
    EVAL_PERL    => 1,
};

my $template = Template->new($config);

my $input = 'form.html';

my %vars = (
    'items' => $items,
);

$template->process($input, \%vars)
    || die $template->error();

1;