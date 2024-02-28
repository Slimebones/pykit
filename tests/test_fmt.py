from pykit.fmt import FormatUtils


def test_kebabify():
    assert FormatUtils.kebabify("wow_hello") == "wow-hello"


def test_snakefy():
    assert FormatUtils.snakefy("HelloWorld") == "hello_world"
    assert FormatUtils.snakefy("hello_world") == "hello_world"
    assert FormatUtils.snakefy("StandardHTTPS") == "standard_https"
    assert FormatUtils.snakefy("standardHTTPS") == "standard_https"
    assert \
        FormatUtils.snakefy("standardHTTPSToHTTP") \
            == "standard_https_to_http"
    assert FormatUtils.snakefy("HTTPSToHTTPGen") == "https_to_http_gen"
    assert FormatUtils.snakefy("HelloWorldD") == "hello_world_d"
    assert FormatUtils.snakefy("H") == "h"
    assert FormatUtils.snakefy("HE") == "he"
    assert FormatUtils.snakefy("HE_WO") == "he_wo"
    assert FormatUtils.snakefy("_hello_worldAgain_") == "_hello_world_again_"


def test_pascalify():
    assert FormatUtils.pascalify("hello_world") == "HelloWorld"
    assert FormatUtils.pascalify("HelloWorld") == "HelloWorld"
    assert FormatUtils.pascalify("hello_WORLD_AGAIN") == "HelloWORLDAGAIN"
    assert FormatUtils.pascalify("_helloworld_again_") == "_HelloworldAgain_"
    assert FormatUtils.pascalify("h") == "H"
    assert FormatUtils.pascalify("h_e") == "HE"
    assert FormatUtils.pascalify("h_e_world") == "HEWorld"
    assert \
        FormatUtils.pascalify("____hello_world____") == "____HelloWorld____"
    assert \
        FormatUtils.pascalify("____hello123_w23orld____") \
            == "____Hello123W23orld____"
    assert \
        FormatUtils.pascalify("____56hello1_w23orld____") \
            == "____56hello1W23orld____"
