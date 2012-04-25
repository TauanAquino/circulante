#coding: utf-8

#XXX: melhorar tratamento de erros

import io
import sys
from django.core.management.base import BaseCommand, CommandError

from circulante.catalogo.models import Publicacao, Credito

class Command(BaseCommand):
    args = '<arq_delimitado_por_tabs> [<encoding>]'
    help = 'Import all data from library (default encoding: utf-8)'

    def handle(self, *args, **options):
        if len(args) < 1:
            raise CommandError('Please enter with the file name to import')
        file_name = args[0]
        if len(args) == 2:
            encoding = args[1]
        else:
            encoding = 'utf-8'
        with io.open(file_name,'r', encoding=encoding) as enter_file:
            qty_registers = 0
            try:
                for line in enter_file:
                    line = line.rstrip()

                    if not line:
                        continue
                    parts = line.split('\t')
                    id_padrao = None
                    autores = ''
                    if len(parts) >= 3:
                        id_padrao, num_paginas, titulo = parts[:3]
                    if len(parts) == 4:
                        autores = parts[3]
                    if id_padrao is None:
                        raise CommandError(repr(parts))
                    num_paginas = int(num_paginas)
                    pub = Publicacao(id_padrao = id_padrao, 
                                    titulo = titulo,
                                    num_paginas = num_paginas)
                    pub.save()
                    
                    for autor in autores.split('/'):
                        autor = autor.strip()
                        if not autor:
                            continue
                        cre = Credito(nome = autor, publicacao = pub)
                        cre.save()
                    qty_registers += 1
                    
            except UnicodeDecodeError as exc:
                msg = 'Incorrect encoding: "{0.reason}" position:{0.start}'
                raise CommandError(msg.format(exc))
        self.stdout.write('Importing %s registers\n' % qty_registers)

