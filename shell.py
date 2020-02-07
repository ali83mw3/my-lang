import toriz

print('\tWelcome To Torab for basic interpreter\n\n\tCopy Right By Ali Reza Torabi\n~~~~~~~~~~~for exit just type exit~~~~~~~~~~')
while True:
    text = input('t4b ->')
    
    if text.lower() == 'exit':
        break
    
    result,error = toriz.run('<stdin>',text)
    if error:
        print(error.as_string())
    else: 
        print(result)
            
    