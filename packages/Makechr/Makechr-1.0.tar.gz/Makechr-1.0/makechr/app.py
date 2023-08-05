import errors
import image_processor
import memory_importer
import ppu_memory
import rom_builder
import view_renderer


class Application(object):
  def run(self, img, args):
    traversal = self.get_traversal(args.traversal_strategy)
    processor = image_processor.ImageProcessor()
    processor.process_image(img, args.palette, args.bg_color, traversal,
                            args.is_sprite, args.is_locked_tiles)
    if processor.err().has():
      es = processor.err().get()
      print('Found {0} error{1}:'.format(len(es), 's'[len(es) == 1:]))
      for e in es:
        print('{0} {1}'.format(type(e).__name__, e))
      if args.error_outfile:
        print('Errors displayed in "{0}"'.format(args.error_outfile))
        errs = processor.err().get(include_dups=True)
        renderer = view_renderer.ViewRenderer()
        renderer.create_error_view(args.error_outfile, img, errs)
      return
    self.create_views(processor.ppu_memory(), processor, args, img)
    self.create_output(processor.ppu_memory(), args, traversal)
    if args.show_stats:
      self.show_stats(processor.ppu_memory(), processor, args)

  def get_traversal(self, strategy):
    if not strategy or strategy == 'h' or strategy == 'horizontal':
      return 'horizontal'
    elif strategy == 'b' or strategy == 'block':
      return 'block'
    else:
      raise errors.UnknownStrategy(strategy)

  def read_memory(self, filename, args):
    importer = memory_importer.MemoryImporter()
    mem = importer.read(filename)
    self.create_output(mem, args, self.get_traversal(None))

  def create_views(self, mem, processor, args, img):
    if args.palette_view:
      renderer = view_renderer.ViewRenderer()
      renderer.create_palette_view(args.palette_view, mem)
    if args.colorization_view:
      renderer = view_renderer.ViewRenderer()
      renderer.create_colorization_view(args.colorization_view,
          mem, processor.artifacts(), processor.color_manifest())
    if args.reuse_view:
      renderer = view_renderer.ViewRenderer()
      renderer.create_reuse_view(args.reuse_view, mem, processor.nt_count())
    if args.nametable_view:
      renderer = view_renderer.ViewRenderer()
      renderer.create_nametable_view(args.nametable_view, mem)
    if args.chr_view:
      renderer = view_renderer.ViewRenderer()
      renderer.create_chr_view(args.chr_view, mem)
    if args.grid_view:
      renderer = view_renderer.ViewRenderer()
      renderer.create_grid_view(args.grid_view, img)

  def create_output(self, mem, args, traversal):
    if args.order is None and args.is_sprite:
      order = 1
    else:
      order = args.order
    if args.output and args.output.endswith('.o'):
      mem.save_valiant(args.output, order, traversal, args.is_sprite)
    else:
      out_tmpl = args.output or '%s.dat'
      if not '%s' in out_tmpl:
        raise errors.CommandLineArgError('output needs "%s" in its template')
      mem.save_template(out_tmpl, order, args.is_sprite)
    if args.compile:
      builder = rom_builder.RomBuilder()
      builder.build(mem.get_writer(), args.compile)

  def show_stats(self, mem, processor, args):
    print('Number of dot-profiles: {0}'.format(len(processor.dot_manifest())))
    print('Number of tiles: {0}'.format(len(mem.chr_data)))
    pal = mem.palette_spr if args.is_sprite else mem.palette_nt
    print('Palette: {0}'.format(pal))
