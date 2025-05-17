from minesweeper import Sentence

test_sentence = Sentence({(0,0),(0,1),(0,2)},2)

print('Sentence:', test_sentence)

print('Cells in sentence:', test_sentence.cells)
print('Count in sentence:', test_sentence.count)
print('Known mines:',test_sentence.known_mines())
print('Known safes:', test_sentence.known_safes())
print('Marking (0,0) as mine..')
test_sentence.mark_mine((0,0))
print('Done! New sentence:', test_sentence)
print('Known mines:',test_sentence.known_mines())
print('Known safes:', test_sentence.known_safes())
print('Marking (0,1) as safe..')
test_sentence.mark_safe((0,1))
print('Done! New sentence:', test_sentence)
print('Known mines:',test_sentence.known_mines())
print('Known safes:', test_sentence.known_safes())