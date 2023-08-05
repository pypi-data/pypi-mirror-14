github_repo=git@github.com:AndreaCensi/procgraph.git

include docs.mk

packages=procgraph.components 
packages+=procgraph_cv
packages+=procgraph_foo
packages+=procgraph_hdf
packages+=procgraph_images
packages+=procgraph_io_misc
packages+=procgraph_mpl
packages+=procgraph_mplayer
packages+=procgraph_numpy_ops
packages+=procgraph_pil
packages+=procgraph_robotics
packages+=procgraph_ros
packages+=procgraph_signals
packages+=procgraph_statistics
packages+=procgraph_yaml

	
pgdoc:	
	pgdoc --translate `pwd`/..=https://github.com/AndreaCensi/procgraph/blob/master  --output source/pgdoc.inc $(packages)
