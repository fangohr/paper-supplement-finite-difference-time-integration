OBJDIR := output

$(OBJDIR):
	mkdir -p $(OBJDIR)

relax: std_4_init_magnetisation.omf

std_4_init_magnetisation.omf: | $(OBJDIR)
	oommf boxsi std_4_init.mif
	@echo Moving generated files to $(OBJDIR) directory.
	mv std_4_init.odt $(OBJDIR)
	mv std_4_init-Oxs_MinDriver-Spin-*.omf $(OBJDIR)
	@echo Getting a copy of relaxed magnetisation needed for dynamics.
	cp $(OBJDIR)/std_4_init-Oxs_MinDriver-Spin-000201-*.omf $@

dynamics: std_4_dynamics_field_2.txt

std_4_dynamics_field_2.txt: std_4_init_magnetisation.omf
	oommf boxsi std_4_field_2.mif
	@echo Extracting dynamics.
	oommf odtcols 18 1 14 15 16 < std_4_field_2.odt > $@
	@echo Moving generated files to $(OBJDIR) directory.
	mv std_4_field_2.odt $(OBJDIR)
	mv std_4_field_2-Oxs_TimeDriver-Spin-*.omf $(OBJDIR)

images:
	tclsh oommf.tcl avf2ppm std_4_field_1.omf -config std_4_plot.config \
		-opatexp "Oxs_TimeDriver-Magnetization-([0-9]+)-.*.omf" \
		-opatsub "\1.png" -filter pnmtopng 

movie:
	ffmpeg -start_number 0 -i std_4_field_1-%07d.png -r 25 -c:v libx264 \
		-pix_fmt yuv420p -qmin 0 -qmax 32 -an std_4_field_1.mp4

.PHONY: relax dynamics
