images:
	tclsh oommf.tcl avf2ppm std_4_field_1.omf -config std_4_plot.config \
		-opatexp "Oxs_TimeDriver-Magnetization-([0-9]+)-.*.omf" \
		-opatsub "\1.png" -filter pnmtopng 

movie:
	ffmpeg -start_number 0 -i std_4_field_1-%07d.png -r 25 -c:v libx264 \
		-pix_fmt yuv420p -qmin 0 -qmax 32 -an std_4_field_1.mp4
