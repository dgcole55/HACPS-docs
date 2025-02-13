

Part 3:  Wordle Server
======================

The purpose of the Wordle server is to determine the ``character_state`` of the letters of a word that has been input; that is, we need to determine if the letter is correct and in the correct location, correct but in the wrong location, or just incorrect.  The Wordle server communicates with the client, because it is the client that is collecting letters in a table.  

A bit about the table.  The table is defined as an array of size ``NUM_TRIES`` -by- ``WORD_LENGTH``.  Those constants and the ``character_state`` I will mention shortly are defined in ``wordle.h``.

In ``client.c``, the table is defined to be

.. code-block:: c

    static struct wordle_char table[NUM_TRIES][WORD_LENGTH];

Each entry in the table is type ``wordle_char``, which is a structure that holds two things:  the character and the ``character_state``.

.. code-block:: c

    struct wordle_char {
        int ch;
        enum character_state state;
    };

Finally, the character state is an enumeration, and is defined in ``wordle.h``.

.. code-block:: c

    enum character_state {
        CORRECT_PLACEMENT = 0, // Correct character, in the correct index of the word.
        INCORRECT_PLACEMENT = 1, // Correct character, in the incorrect index of the word.
       INCORRECT = 2, // Character does not appear in the word.
    };

The purpose of the wordle server is to take a word and go through it letter by letter and determine the character state of each.  

Wordle Server Protection Domain
-------------------------------

Just like the serial server and the client, the wordle server needs to have its own protection domain.

.. code-block:: xml

    <protection_domain name="wordle_server" priority="254" pp="true">
        <program_image path="wordle_server.elf" />
    </protection_domain>

Client-Wordle Server Channel
-------------------------------

So that the client and the wordle server can communicate, we will need to setup a channel.  

.. code-block:: xml

    <channel>
        <end pd="client" id="2" />
        <end pd="wordle_server" id="1" />
    </channel>

Protected Procedure Call
------------------------

We do not need to setup a memory-region for this.  In this case, we will use the protected procedure call to send data between the client and the Wordle server.  When we do this, seL4 allows for 64 words (probably 512 bytes) to be shared.  

The protected procedure call is invoked by the client in ``wordle_server_send()``.

.. code-block:: c

    void wordle_server_send() {
        for (int i = 0; i < WORD_LENGTH; i++) {
            microkit_mr_set(i, table[curr_row][i].ch);
        }
        //
        microkit_ppcall(WORDLE_CHANNEL, microkit_msginfo_new(0, WORD_LENGTH));
        //
        for (int i = 0; i < WORD_LENGTH; i++) {
            table[curr_row][i].state = microkit_mr_get(i);
        }
    }   

This does three things.  

1.  It uses ``microkit_mr_set`` to put each character in the table into a shared memory region that is created by Microkit for the protected procedure call.  This can be up to the 64 word limit.
2.  It calls the protected procedure.
3.  Once the protected procedure is finished, it then gets the character state of each character that was put in memory by the Wordle server.

The protected procedure call is defined in ``wordle_server.c`` as 

.. code-block::


    microkit_msginfo protected(microkit_channel channel, microkit_msginfo msginfo) {
        for (int i = 0; i < WORD_LENGTH; i++) {
            char ch = microkit_mr_get(i);
            microkit_mr_set(i, char_to_state(ch, word, i));
        }
        return microkit_msginfo_new(0, WORD_LENGTH);
    }

When invoked by the client it goes letter by letter, each stored in a memory region that is created by the procedure call, and sets the character state for each.

Now when you finish typing a word and press return, you should get an output that shows letters as green, yellow, or white, depending on their character state.  By the way, the default Wordle word is 'hello'.  In the next part, we will create a Linux virtual machine to go and get a new word for each time you run the game.


