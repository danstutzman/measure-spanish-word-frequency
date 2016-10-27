# coding=UTF-8
# Note: if you get UnicodeEncodeError, run with PYTHONIOENCODING=utf_8

import codecs
import glob
import pattern.es
import re
import subprocess

lemma_tag2num_tokens = {}
num_lemma_tag_tokens = 0
i = 0
#for filename in glob.iglob('spanish_in_texas/*.txt'):
for filename in subprocess.check_output(['find', 'CORLEC_TXT_FINAL/', '-name', '*.txt']).split('\n'):
  i += 1
  #if i > 1: break
  if filename == '':
    continue
  print filename

  language2bad_words = {}
  language2bad_words = {'en': {}, 'es': {}}
  #for language in ['en', 'es']:
  #  with open(filename) as f:
  #    bad_words = {}
  #    proc = subprocess.Popen(['aspell', '-a', '-l', language, '--sug-mode=ultra'],
  #      stdin=subprocess.PIPE, stdout=subprocess.PIPE)
  #    out = proc.communicate(f.read())[0]
  #    for line in re.split(r'\n', out):
  #      if line.startswith('&'):
  #        bad_word = line.split(' ')[1]
  #        bad_words[bad_word] = True
  #    language2bad_words[language] = bad_words
  
  with codecs.open(filename, 'r', 'utf8') as f:
    for line in f:
      line = line.strip()

      if line != '':
        line = re.sub(r'^>>[si]: ', '', line)
        line = re.sub(u'[¿¡]', '', line)
        sentences = pattern.es.parsetree(line, lemmata=True)
        for sentence in sentences:
          num_en_words = sum(0 if language2bad_words['en'].get(word.string) else 1 \
              for word in sentence)
          num_es_words = sum(0 if language2bad_words['es'].get(word.string) else 1 \
              for word in sentence)
          if num_es_words >= num_en_words:
            for word in sentence:
              if re.match(u'^[a-záéíóúñü-]+$', word.lemma):
                lemma_tag = word.lemma + '/' + word.tag
                #if lemma not in ['.', ',', '?', '...', '!', '[', ']', 'no.', ';']:
                #  print lemma
                if not lemma_tag in lemma_tag2num_tokens:
                  lemma_tag2num_tokens[lemma_tag] = 0
                lemma_tag2num_tokens[lemma_tag] += 1
                num_lemma_tag_tokens += 1

for lemma_tag in sorted(lemma_tag2num_tokens, key=lambda lemma_tag: lemma_tag2num_tokens[lemma_tag]):
  lemma, tag = lemma_tag.split('/')
  #if not tag in ['DT', 'IN', 'WP$', 'CC', 'PRP', 'PRP$']:
  if True:
    print u'%-20s %-4s %6d'.encode('utf8') % \
      (lemma, tag,
      lemma_tag2num_tokens[lemma_tag] * 1000000.0 / num_lemma_tag_tokens)
