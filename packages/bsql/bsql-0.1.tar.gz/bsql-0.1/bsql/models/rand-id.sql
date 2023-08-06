/* rand_id() -- return a random character string: useful for generating ids and passwords
    parameters: 
      length, defaults to 8 
      base, defaults to 62
    examples:
      rand_id(6, 16) -- will return a 6-character hex number = random RGB color
      rand_id(6, 73) -- one of 151 billion URL slugs = a respectable URL shortener
      rand_id(8, 62) -- alphanumeric password, 218 trillion possibilities
      rand_id(8, 73) -- one of 800 quadrillion passwords, a bit more secure
      rand_id(16, 16) -- 128-bit hex number, 1.8e19 possibilities, as secure as most banks.

  by Sean Harrison <sah@blackearthgroup.com>
  ------------------------------------------------------------------------ */
create or replace function rand_id(int, int) returns varchar as $$
  declare
    length  alias for $1; -- the length of the id to create
    base    alias for $2; -- the base number of characters
    chars   varchar;  -- values to use as a base
    id      varchar;  -- the resulting id string
  begin
    /* A 8-character id with base 62 has 62^8 ~ 218 trillion possibilities. Enough for most uses.
       Common bases:
        10  -- integers
        16  -- hex numbers (0-f)
        36  -- integers + lowercase ascii
        62  -- integers + lowercase ascii + uppercase
        73  -- integers + lowercase ascii + uppercase + URL-path-safe punctuation
    */
    chars := '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ$-_.+!*",()';
    id := '';
    for i in 1..length loop
      id := id || substring(chars from ceiling(random()*base)::int for 1);
    end loop;
    return id;
  end;  
$$ language 'plpgsql';

create or replace function rand_id(int) returns varchar as $$
  -- $1 is length, base defaults to 62
  select rand_id($1, 62);
$$ language 'sql';

create or replace function rand_id() returns varchar as $$
  -- length defaults to 8, base defaults to 62. 62^8 ~ 218 trillion
  select rand_id(8, 62);
$$ language 'sql';
