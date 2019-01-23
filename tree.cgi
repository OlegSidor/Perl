#!/usr/bin/perl
use strict;
use warnings FATAL => 'all';
use Data::Dumper;
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use Template;

print "Content-Type: text/html\n\n";
print "<meta charset='UTF-8'>";

=head1
    Name AbillsTree
    Version 1.0
    Description
        Show Abills documentation tree

=cut

our $start_folder = "/usr/abills/";
my $q = CGI->new();

my $show = $q->param('show');
if ($show) {
  print "<a href='/tree.cgi'><- Назад</a><br><br><br>";
  my $doc = qx/perldoc $show/;
  $doc =~ s/\n/<br>/g;
  print $doc;
  exit;
}

my @tree;
generate($start_folder, \@tree);
#********************************************
=head2 generate ($folder, $treeHash) - Generate tree function

  Argunents:
    $folder - start folder
    $treeHash - tree hash

  Returns:
    tree hash

  Example:
    generate("/path/to/folder/");

=cut
#********************************************
sub generate {
  my ($folder, $tree_hash) = @_;
  opendir(my $dir, $folder);
  for (readdir($dir)) {
    if ($_ ne '.' && $_ ne '..') {
      if (extension($folder . $_) eq ".pm" || -d $folder . $_) {
        my %item;
        if (-d $folder . $_) {
          $item{'name'} = $_;
          $item{'children'} = [];
          generate($folder . $_ . '/', $item{"children"});
        }
        else {
          my $path = $folder . $_;
          $item{"name"} = $_;
          $item{'children'} = [];
          $item{"url"} = $path;
        }
        if (scalar(@{$item{'children'}}) != 0 || $item{'url'}) {
          push(@$tree_hash, \%item);
        }
      }
    }
  }
  closedir($dir);
  return 1;
}

=head1 extension($path) - get extension from path function

  Arguments:
    $path - path to file
    file extention
  Returns:
    extention of file
  Expample:
    extension("/path/to/file.txt");

=cut
#**********************************
sub extension {
  my $path = shift;
  $path =~ / \. [a-z0-9]+ $ /xi;
  $& // '';
}


my $config = {
  INCLUDE_PATH => '.',
  INTERPOLATE  => 1,
  POST_CHOMP   => 1,
  PRE_PROCESS  => '',
  EVAL_PERL    => 1,
};

my $template = Template->new($config);

my $input = 'tree.html';

my %vars = (
  'items' => \@tree,
);

$template->process($input, \%vars)
  || die $template->error();

1;