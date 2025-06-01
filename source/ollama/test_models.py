from ollama_client import OllamaClient

# List of LLM models to test
MODELS = [
    'llama3.2:3b',
    'llama3.1:8b',
    'gemma3:12b',
    'qwen3:8b']

PROMPT_FILE = 'test_prompts.txt'    # File containing list of prompts to test
OUTPUT_DIRECTORY = 'test_outputs'   # Output directory to store test files
NUM_TESTS = 25                      # Number of times to run test routine


def main():
    # Create a list of prompts from prompt file
    fin = open(PROMPT_FILE, 'r')
    prompts = fin.readlines()

    for i in range(0, NUM_TESTS):
        fout = open(OUTPUT_DIRECTORY + 'test_output_%s.txt' % i, 'w')
        print("Running test #%s:" % i)

        for model in MODELS:
            client = OllamaClient("http://localhost:11434", model)
            fout.write("<%s>\n" % model)

            for j, p in enumerate(prompts):
                print("\tSending prompt #%s to %s" % (j, model))
                fout.write("<test%s>\n" % j)
                fout.write("<prompt>\n%s</prompt>\n" % p)
                fout.write("<response>\n")
                response = client.query(p)
                fout.write("%s\n" % response)
                fout.write("</response>\n")
                fout.write("</test%s>\n" % j)

            fout.write("</%s>\n" % model)
        fout.close()


if __name__ == '__main__':
    main()
